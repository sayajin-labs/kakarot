import logging

import pytest
from starkware.starknet.testing.contract import StarknetContract

from tests.integration.helpers.helpers import hex_string_to_bytes_array
from tests.integration.helpers.wrap_kakarot import get_contract, wrap_for_kakarot
from tests.utils.reporting import traceit

logger = logging.getLogger()


@pytest.fixture(scope="module")
def deploy_solidity_contract(starknet, contract_account_class, kakarot):
    """
    Fixture to deploy a solidity contract in kakarot. The returned contract is a modified
    web3.contract instance with an added `contract_account` attribute that return the actual
    underlying kakarot contract account.
    """

    deployed_contracts = {}

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
        if contract_name in deployed_contracts:
            return deployed_contracts[contract_name]
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
        contract_account = StarknetContract(
            starknet.state,
            contract_account_class.abi,
            starknet_contract_address,
            tx,
        )

        kakarot_contract = wrap_for_kakarot(
            contract, kakarot, tx.result.evm_contract_address
        )
        setattr(kakarot_contract, "contract_account", contract_account)
        deployed_contracts[contract_name] = kakarot_contract

        return kakarot_contract

    yield _factory

    logger.info(f"Deployed solidity contracts: {list(deployed_contracts)}")
    deployed_contracts = {}


@pytest.fixture
def addresses():
    _addresses = list(range(4))
    return [{"int": _a, "hex": "0x" + "0" * 39 + str(_a)} for _a in _addresses]


@pytest.fixture
def kakarot_snapshot(kakarot):
    state = kakarot.state.copy()
    yield kakarot
    kakarot.state = state
