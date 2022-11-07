from textwrap import wrap
from time import time

import pytest
import pytest_asyncio
from starkware.starknet.testing.contract import DeclaredClass, StarknetContract
from starkware.starknet.testing.starknet import Starknet


@pytest_asyncio.fixture(scope="module")
async def zk_evm(
    starknet: Starknet, eth: StarknetContract, contract_account_class: DeclaredClass
):
    start = time()
    _zk_evm = await starknet.deploy(
        source="./src/kakarot/kakarot.cairo",
        cairo_path=["src"],
        disable_hint_validation=True,
        constructor_calldata=[
            1,
            eth.contract_address,
            contract_account_class.class_hash,
        ],
    )
    evm_time = time()
    print(f"\nzkEVM deployed in {evm_time - start:.2f}s")
    return _zk_evm


@pytest_asyncio.fixture(scope="module", autouse=True)
async def set_account_registry(zk_evm, account_registry):
    await account_registry.transfer_ownership(zk_evm.contract_address).execute(
        caller_address=1
    )
    await zk_evm.set_account_registry(
        registry_address_=account_registry.contract_address
    ).execute(caller_address=1)
    yield
    await account_registry.transfer_ownership(1).execute(
        caller_address=zk_evm.contract_address
    )


[
    "0xa9059cbb000000000000000000000000abde100709ca8e90190f4e6f86d387e97293851a0000000000000000000000000000000000000000000000000000000000000005"
]

test_cases = [
    {
        "params": {
            "code": "608060405234801561001057600080fd5b5060405161080d38038061080d83398101604081905261002f91610197565b815161004290600090602085019061005e565b50805161005690600190602084019061005e565b505050610248565b82805461006a906101f7565b90600052602060002090601f01602090048101928261008c57600085556100d2565b82601f106100a557805160ff19168380011785556100d2565b828001600101855582156100d2579182015b828111156100d25782518255916020019190600101906100b7565b506100de9291506100e2565b5090565b5b808211156100de57600081556001016100e3565b600082601f830112610107578081fd5b81516001600160401b038082111561012157610121610232565b6040516020601f8401601f191682018101838111838210171561014657610146610232565b604052838252858401810187101561015c578485fd5b8492505b8383101561017d5785830181015182840182015291820191610160565b8383111561018d57848185840101525b5095945050505050565b600080604083850312156101a9578182fd5b82516001600160401b03808211156101bf578384fd5b6101cb868387016100f7565b935060208501519150808211156101e0578283fd5b506101ed858286016100f7565b9150509250929050565b60028104600182168061020b57607f821691505b6020821081141561022c57634e487b7160e01b600052602260045260246000fd5b50919050565b634e487b7160e01b600052604160045260246000fd5b6105b6806102576000396000f3fe608060405234801561001057600080fd5b50600436106100935760003560e01c806340c10f191161006657806340c10f19146100fe57806370a082311461011357806395d89b4114610126578063a9059cbb1461012e578063dd62ed3e1461014157610093565b806306fdde0314610098578063095ea7b3146100b657806318160ddd146100d657806323b872dd146100eb575b600080fd5b6100a0610154565b6040516100ad91906104a4565b60405180910390f35b6100c96100c4366004610470565b6101e2565b6040516100ad9190610499565b6100de61024c565b6040516100ad91906104f7565b6100c96100f9366004610435565b610252565b61011161010c366004610470565b610304565b005b6100de6101213660046103e2565b61033d565b6100a061034f565b6100c961013c366004610470565b61035c565b6100de61014f366004610403565b6103a9565b600080546101619061052f565b80601f016020809104026020016040519081016040528092919081815260200182805461018d9061052f565b80156101da5780601f106101af576101008083540402835291602001916101da565b820191906000526020600020905b8154815290600101906020018083116101bd57829003601f168201915b505050505081565b3360008181526004602090815260408083206001600160a01b038716808552925280832085905551919290917f8c5be1e5ebec7d5bd14f71427d1e84f3dd0314c0f7b2291e5b200ac8c7c3b9259061023b9086906104f7565b60405180910390a350600192915050565b60025481565b6001600160a01b038316600090815260046020908152604080832033845290915281205460001981146102ae576102898382610518565b6001600160a01b03861660009081526004602090815260408083203384529091529020555b6001600160a01b038516600090815260036020526040812080548592906102d6908490610518565b9091555050506001600160a01b03831660009081526003602052604090208054830190555060019392505050565b80600260008282546103169190610500565b90915550506001600160a01b03909116600090815260036020526040902080549091019055565b60036020526000908152604090205481565b600180546101619061052f565b3360009081526003602052604081208054839190839061037d908490610518565b9091555050506001600160a01b0382166000908152600360205260409020805482019055600192915050565b600460209081526000928352604080842090915290825290205481565b80356001600160a01b03811681146103dd57600080fd5b919050565b6000602082840312156103f3578081fd5b6103fc826103c6565b9392505050565b60008060408385031215610415578081fd5b61041e836103c6565b915061042c602084016103c6565b90509250929050565b600080600060608486031215610449578081fd5b610452846103c6565b9250610460602085016103c6565b9150604084013590509250925092565b60008060408385031215610482578182fd5b61048b836103c6565b946020939093013593505050565b901515815260200190565b6000602080835283518082850152825b818110156104d0578581018301518582016040015282016104b4565b818111156104e15783604083870101525b50601f01601f1916929092016040019392505050565b90815260200190565b600082198211156105135761051361056a565b500190565b60008282101561052a5761052a61056a565b500390565b60028104600182168061054357607f821691505b6020821081141561056457634e487b7160e01b600052602260045260246000fd5b50919050565b634e487b7160e01b600052601160045260246000fdfea26469706673582212204e53876a7abf080ce7b38dffe1572ec4843a83c565efd2feeb856984b5af6fb764736f6c634300080000330000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000008000000000000000000000000000000000000000000000000000000000000000074b616b61726f74000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000003534a4e0000000000000000000000000000000000000000000000000000000000",
            "mint": "40c10f1900000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000164",
            "approve": "095ea7b3000000000000000000000000000000000000000000000000000000000000000100000000000000000000000000000000000000000000000000000000000f4240",
            "allowance": "dd62ed3e00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000001",
            "transferFrom": "23b872dd00000000000000000000000000000000000000000000000000000000000000020000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000000000000000000a",
            "transfer": "a9059cbb00000000000000000000000000000000000000000000000000000000000000030000000000000000000000000000000000000000000000000000000000000005",
            "balanceOf": "70a082310000000000000000000000000000000000000000000000000000000000000001",
            "totalSupply": "18160ddd",
            "name": "06fdde03",
            "symbol": "95d89b41",
            "stack": "",
            "memory": "",
            "return_value": "0000000000000000000000000000000000000000000000000000000000000005",
        },
        "id": "solmate_erc20_all_test",
    },
]


params = [pytest.param(case.pop("params"), **case) for case in test_cases]


@pytest.mark.asyncio
class TestZkEVM:
    @staticmethod
    def int_to_uint256(value):
        low = value & ((1 << 128) - 1)
        high = value >> 128
        return low, high

    @pytest.mark.parametrize(
        "params",
        params[:1],
        # TODO: not sure how of those we want to re-run with the execute_at_address because it is very slow
        # TODO: This is a magic number.
    )
    async def test_erc20(
        self, starknet: Starknet, zk_evm, params, contract_account_class: DeclaredClass
    ):
        Uint256 = zk_evm.struct_manager.get_contract_struct("Uint256")

        print("DEPLOYING CONTRACT")
        res = await zk_evm.execute_at_address(
            address=0,
            calldata=[int(b, 16) for b in wrap(params["code"], 2)],
        ).execute(caller_address=1)

        evm_contract_address = res.result.evm_contract_address
        starknet_contract_address = res.result.starknet_contract_address

        print("INITIATING CONTRACT")
        res = await zk_evm.initiate(
            evm_address=evm_contract_address, starknet_address=starknet_contract_address
        ).execute(caller_address=1)

        print("CALLING mint TX")
        res = await zk_evm.execute_at_address(
            address=evm_contract_address,
            calldata=[int(b, 16) for b in wrap(params["mint"], 2)],
        ).execute(caller_address=2)

        print("CALLING approve TX")
        res = await zk_evm.execute_at_address(
            address=evm_contract_address,
            calldata=[int(b, 16) for b in wrap(params["approve"], 2)],
        ).execute(caller_address=2)

        print("CALLING allowance TX")
        res = await zk_evm.execute_at_address(
            address=evm_contract_address,
            calldata=[int(b, 16) for b in wrap(params["allowance"], 2)],
        ).execute(caller_address=2)

        print("CALLING transferFrom TX")
        res = await zk_evm.execute_at_address(
            address=evm_contract_address,
            calldata=[int(b, 16) for b in wrap(params["transferFrom"], 2)],
        ).execute(caller_address=1)

        print("CALLING Transfer")
        res = await zk_evm.execute_at_address(
            address=evm_contract_address,
            calldata=[int(b, 16) for b in wrap(params["transfer"], 2)],
        ).execute(caller_address=1)

        print("CHECKING balanceOf TX")
        res = await zk_evm.execute_at_address(
            address=evm_contract_address,
            calldata=[int(b, 16) for b in wrap(params["balanceOf"], 2)],
        ).execute(caller_address=1)

        # assert res.result.stack == [
        #     Uint256(*self.int_to_uint256(int(s)))
        #     for s in (params["stack"].split(",") if params["stack"] else [])
        # ]
        assert res.result.return_data == [
            int(m, 16) for m in wrap(params["return_value"], 2)
        ]
