# source: https://github.com/OpenZeppelin/cairo-contracts/tree/main/tests/signers.py

from typing import Tuple
from starkware.starknet.core.os.transaction_hash.transaction_hash import TransactionHashPrefix
from starkware.starknet.core.os.contract_address.contract_address import (
    calculate_contract_address_from_hash,
)
from starkware.starknet.definitions.general_config import StarknetChainId
from starkware.starknet.services.api.gateway.transaction import InvokeFunction, DeployAccount
from starkware.starknet.business_logic.transaction.objects import InternalTransaction, InternalDeclare, TransactionExecutionInfo
from starkware.starknet.public.abi import get_selector_from_name
import eth_keys
from tests.utils.bits import to_uint
from starkware.starknet.core.os.transaction_hash.transaction_hash import calculate_transaction_hash_common

TRANSACTION_VERSION = 1

def get_transaction_hash(prefix, account, calldata, nonce, max_fee, version, chain_id):
    """Compute the hash of a transaction."""
    return calculate_transaction_hash_common(
        tx_hash_prefix=prefix,
        version=version,
        contract_address=account,
        entry_point_selector=0,
        calldata=calldata,
        max_fee=max_fee,
        chain_id=chain_id,
        additional_data=[nonce],
    )

def from_call_to_call_array(calls):
    """Transform from Call to CallArray."""
    call_array = []
    calldata = []
    for _, call in enumerate(calls):
        assert len(call) == 3, "Invalid call parameters"
        entry = (
            call[0],
            get_selector_from_name(call[1]),
            len(calldata),
            len(call[2]),
        )
        call_array.append(entry)
        calldata.extend(call[2])
    return (call_array, calldata)

classHash = 0x1

class BaseSigner():
    async def send_transaction(self, account, to, selector_name, calldata, nonce=None, max_fee=0):
        return await self.send_transactions(account, [(to, selector_name, calldata)], nonce, max_fee)

    async def send_transactions(
        self,
        account,
        calls,
        nonce=None,
        max_fee=0
    ) -> TransactionExecutionInfo:
        raw_invocation = get_raw_invoke(account, calls)
        state = raw_invocation.state

        if nonce is None:
            nonce = await state.state.get_nonce_at(account.contract_address)

        transaction_hash = get_transaction_hash(
            prefix=TransactionHashPrefix.INVOKE,
            account=account.contract_address,
            calldata=raw_invocation.calldata,
            version=TRANSACTION_VERSION,
            chain_id=StarknetChainId.TESTNET.value,
            nonce=nonce,
            max_fee=max_fee,
        )

        signature = self.sign(transaction_hash)

        external_tx = InvokeFunction(
            contract_address=account.contract_address,
            calldata=raw_invocation.calldata,
            entry_point_selector=None,
            signature=signature,
            max_fee=max_fee,
            version=TRANSACTION_VERSION,
            nonce=nonce,
        )

        tx = InternalTransaction.from_external(
            external_tx=external_tx, general_config=state.general_config
        )
        execution_info = await state.execute_tx(tx=tx)
        return execution_info

    async def deploy_account(
        self,
        state,
        calldata,
        salt=0,
        nonce=0,
        max_fee=0,
    ) -> TransactionExecutionInfo:
        account_address = calculate_contract_address_from_hash(
            salt=salt,
            class_hash=self.class_hash,
            constructor_calldata=calldata,
            deployer_address=0
        )

        transaction_hash = get_transaction_hash(
            prefix=TransactionHashPrefix.DEPLOY_ACCOUNT,
            account=account_address,
            calldata=[self.class_hash, salt, *calldata],
            nonce=nonce,
            version=TRANSACTION_VERSION,
            max_fee=max_fee,
            chain_id=StarknetChainId.TESTNET.value
        )

        signature = self.sign(transaction_hash)

        external_tx = DeployAccount(
            class_hash=self.class_hash,
            contract_address_salt=salt,
            constructor_calldata=calldata,
            signature=signature,
            max_fee=max_fee,
            version=TRANSACTION_VERSION,
            nonce=nonce,
        )

        tx = InternalTransaction.from_external(
            external_tx=external_tx, general_config=state.general_config
        )

        execution_info = await state.execute_tx(tx=tx)
        return execution_info

class MockEthSigner(BaseSigner):
    """
    Utility for sending signed transactions to an Account on Starknet, like MockSigner, but using a secp256k1 signature.
    Parameters
    ----------
    private_key : int

    """
    def __init__(self, private_key):
        self.signer = eth_keys.keys.PrivateKey(private_key)
        self.eth_address = int(self.signer.public_key.to_checksum_address(), 0)
        self.class_hash = classHash

    def sign(self, transaction_hash):
        signature = self.signer.sign_msg_hash(
            (transaction_hash).to_bytes(32, byteorder="big"))
        sig_r = to_uint(signature.r)
        sig_s = to_uint(signature.s)
        return [signature.v, *sig_r, *sig_s]


def get_raw_invoke(sender, calls):
    """Return raw invoke, remove when test framework supports `invoke`."""
    call_array, calldata = from_call_to_call_array(calls)
    raw_invocation = sender.__execute__(call_array, calldata)
    return raw_invocation