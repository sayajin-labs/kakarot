import logging
import random
from collections import namedtuple
from typing import List

import pytest
import pytest_asyncio
from starkware.starknet.core.os.contract_address.contract_address import (
    calculate_contract_address_from_hash,
)
from starkware.starknet.testing.contract import StarknetContract
from web3 import Web3

from tests.integration.helpers.helpers import (
    generate_random_private_key,
    hex_string_to_bytes_array,
)
from tests.integration.helpers.wrap_kakarot import get_contract, wrap_for_kakarot
from tests.utils.reporting import traceit

logger = logging.getLogger()


@pytest.fixture(scope="package")
def get_starknet_address(contract_account_class, kakarot):
    """
    Fixture to return the starknet address of a contract deployed by kakarot using CREATE2
    """

    def _factory(salt):
        return calculate_contract_address_from_hash(
            salt=salt,
            class_hash=contract_account_class.class_hash,
            constructor_calldata=[kakarot.contract_address, 0],
            deployer_address=kakarot.contract_address,
        )

    return _factory


@pytest.fixture(scope="package")
def get_solidity_contract(starknet, contract_account_class, kakarot):
    """
    Fixture to attach a a modified web3.contract instance to an already deployed contract_account in kakarot.
    """

    def _factory(
        contract_app, contract_name, starknet_contract_address, evm_contract_address, tx
    ):
        """
        This factory is what is actually returned by pytest when requesting the `get_solidity_contract`
        fixture.
        It creates a web3.contract based on the basename of the target solidity file.
        """
        contract = get_contract(contract_app, contract_name)

        contract_account = StarknetContract(
            starknet.state,
            contract_account_class.abi,
            starknet_contract_address,
            tx,
        )
        contract = get_contract(contract_app, contract_name)
        kakarot_contract = wrap_for_kakarot(
            contract, kakarot, int(evm_contract_address, 16)
        )
        setattr(kakarot_contract, "contract_account", contract_account)
        setattr(kakarot_contract, "evm_contract_address", evm_contract_address)

        return kakarot_contract

    return _factory


@pytest.fixture(scope="package")
def deploy_solidity_contract(kakarot, get_solidity_contract):
    """
    Fixture to deploy a solidity contract in kakarot. The returned contract is a modified
    web3.contract instance with an added `contract_account` attribute that return the actual
    underlying kakarot contract account.
    """

    async def _factory(contract_app, contract_name, *args, **kwargs):
        """
        This factory is what is actually returned by pytest when requesting the `deploy_solidity_contract`
        fixture.
        It creates a web3.contract based on the basename of the target solidity file.
        This contract is deployed to kakarot using the deploy bytecode generated by web3.contract.
        Eventually, the web3.contract is updated such that each function (view or write) targets instead kakarot.

        The args and kwargs are passed as is to the web3.contract.constructor. Only the `caller_address` kwarg is
        is required and filtered out before calling the constructor.
        """
        contract = get_contract(contract_app, contract_name)
        if "caller_address" not in kwargs:
            raise ValueError(
                "caller_address needs to be given in kwargs for deploying the contract"
            )
        caller_address = kwargs["caller_address"]
        del kwargs["caller_address"]
        deploy_bytecode = hex_string_to_bytes_array(
            contract.constructor(*args, **kwargs).data_in_transaction
        )

        with traceit.context(contract_name):
            tx = await kakarot.deploy(bytecode=deploy_bytecode).execute(
                caller_address=caller_address
            )

        starknet_contract_address = tx.result.starknet_contract_address
        evm_contract_address = Web3.toChecksumAddress(
            f"{tx.result.evm_contract_address:040x}"
        )
        return get_solidity_contract(
            contract_app,
            contract_name,
            starknet_contract_address,
            evm_contract_address,
            tx,
        )

    return _factory


Wallet = namedtuple("Wallet", ["address", "private_key", "starknet_address"])


@pytest.fixture(scope="package")
def addresses() -> List[Wallet]:
    """
    Returns a list of addresses to be used in tests.
    Addresses are returned as named tuples with
    - address: the hex string of the EVM address (20 bytes)
    - starknet_address: the corresponding address for starknet (same value but as int)
    """
    random.seed(0)
    private_keys = [generate_random_private_key() for _ in range(4)]
    return [
        Wallet(
            address=private_key.public_key.to_checksum_address(),
            private_key=private_key,
            starknet_address=int(private_key.public_key.to_address(), 16),
        )
        for private_key in private_keys
    ]


@pytest_asyncio.fixture(scope="package")
async def owner(addresses):
    return addresses[0]


@pytest_asyncio.fixture(scope="package")
async def others(addresses):
    return addresses[1:]


@pytest_asyncio.fixture(scope="module")
async def counter(deploy_solidity_contract, owner):
    return await deploy_solidity_contract(
        "Counter", "Counter", caller_address=owner.starknet_address
    )


@pytest_asyncio.fixture(scope="module")
async def plain_opcodes(deploy_solidity_contract, owner, counter):
    return await deploy_solidity_contract(
        "PlainOpcodes",
        "PlainOpcodes",
        counter.evm_contract_address,
        caller_address=owner.starknet_address,
    )


@pytest_asyncio.fixture(scope="module")
async def erc_20(deploy_solidity_contract, owner):
    return await deploy_solidity_contract(
        "Solmate",
        "ERC20",
        "Kakarot Token",
        "KKT",
        18,
        caller_address=owner.starknet_address,
    )
