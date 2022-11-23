// SPDX-License-Identifier: MIT

%lang starknet

// Starkware dependencies

from starkware.cairo.common.alloc import alloc
from starkware.cairo.common.cairo_builtins import HashBuiltin, BitwiseBuiltin
from starkware.starknet.common.syscalls import get_caller_address, get_tx_info
from starkware.cairo.common.uint256 import Uint256

// Internal dependencies
from kakarot.model import model
from utils.utils import Helpers
from kakarot.execution_context import ExecutionContext
from kakarot.stack import Stack
from kakarot.memory import Memory
from kakarot.constants import native_token_address, registry_address
from kakarot.interfaces.interfaces import IEth, IRegistry

// For Felt Packing
from utils.bit_functions import get_byte_in_array, slice_bytes_loop_translator, get_uint256_in_array

// @title Environmental information opcodes.
// @notice This file contains the functions to execute for environmental information opcodes.
// @author @abdelhamidbakhta
// @custom:namespace EnvironmentalInformation
namespace EnvironmentalInformation {
    // Define constants.
    const GAS_COST_ADDRESS = 2;
    const GAS_COST_BALANCE = 100;
    const GAS_COST_ORIGIN = 2;
    const GAS_COST_CALLER = 2;
    const GAS_COST_CALLVALUE = 2;
    const GAS_COST_CALLDATALOAD = 3;
    const GAS_COST_CALLDATASIZE = 2;
    const GAS_COST_CALLDATACOPY = 3;
    const GAS_COST_CODESIZE = 2;
    const GAS_COST_CODECOPY = 3;
    const GAS_COST_RETURNDATASIZE = 2;
    const GAS_COST_RETURNDATACOPY = 3;

    // @notice ADDRESS operation.
    // @dev Get address of currently executing account.
    // @custom:since Frontier
    // @custom:group Environmental Information
    // @custom:gas 2
    // @custom:stack_consumed_elements 0
    // @custom:stack_produced_elements 1
    // @param ctx The pointer to the execution context
    // @return The pointer to the updated execution context.
    func exec_address{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        alloc_locals;

        // Get the current execution contract from the context,
        // convert to Uin256, and push to Stack.
        let address = Helpers.to_uint256(ctx.evm_contract_address);
        let stack: model.Stack* = Stack.push(self=ctx.stack, element=address);
        // Update the execution context.
        let ctx = ExecutionContext.update_stack(self=ctx, new_stack=stack);
        // Increment gas used
        let ctx = ExecutionContext.increment_gas_used(self=ctx, inc_value=GAS_COST_ADDRESS);
        return ctx;
    }

    // @notice BALANCE opcode.
    // @dev Get ETH balance of the specified address.
    // @custom:since Frontier
    // @custom:group Environmental Information
    // @custom:gas 100 || 2600
    // @custom:stack_consumed_elements 1
    // @custom:stack_produced_elements 1
    // @param ctx The pointer to the execution context
    // @return The pointer to the updated execution context.
    func exec_balance{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        alloc_locals;

        // Get the evm address.
        let (stack: model.Stack*, address: Uint256) = Stack.pop(ctx.stack);

        // Get the starknet account address from the evm account address
        let (registry_address_) = registry_address.read();
        let (starknet_contract_address) = IRegistry.get_starknet_contract_address(
            contract_address=registry_address_, evm_contract_address=address.low
        );
        // Get the number of native tokens owned by the given starknet account
        let (native_token_address_) = native_token_address.read();
        let (balance: Uint256) = IEth.balanceOf(
            contract_address=native_token_address_, account=starknet_contract_address
        );

        let stack: model.Stack* = Stack.push(stack, balance);

        // Update the execution context.
        // Update context stack.
        let ctx = ExecutionContext.update_stack(self=ctx, new_stack=stack);
        // Increment gas used.
        let ctx = ExecutionContext.increment_gas_used(self=ctx, inc_value=GAS_COST_BALANCE);
        return ctx;
    }

    // @notice ORIGIN operation.
    // @dev Get execution origination address.
    // @custom:since Frontier
    // @custom:group Environmental Information
    // @custom:gas 2
    // @custom:stack_consumed_elements 0
    // @custom:stack_produced_elements 1
    // @param ctx The pointer to the execution context
    // @return The pointer to the updated execution context.
    func exec_origin{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        alloc_locals;

        // Get the transaction info which contains the starknet origin address
        let (tx_info) = get_tx_info();
        // Get the EVM address from Starknet address
        let (registry_address_) = registry_address.read();
        let (evm_contract_address) = IRegistry.get_evm_contract_address(
            registry_address_, starknet_contract_address=tx_info.account_contract_address
        );
        let origin_address = Helpers.to_uint256(evm_contract_address);

        // Update Context stack
        let stack: model.Stack* = Stack.push(self=ctx.stack, element=origin_address);
        let ctx = ExecutionContext.update_stack(self=ctx, new_stack=stack);
        // Increment gas used
        let ctx = ExecutionContext.increment_gas_used(self=ctx, inc_value=GAS_COST_ORIGIN);
        return ctx;
    }

    // @notice CALLER operation.
    // @dev Get caller address.
    // @custom:since Frontier
    // @custom:group Environmental Information
    // @custom:gas 2
    // @custom:stack_consumed_elements 0
    // @custom:stack_produced_elements 1
    // @param ctx The pointer to the execution context
    // @return The pointer to the updated execution context.
    func exec_caller{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        alloc_locals;
        // Get caller address.
        let (current_address) = get_caller_address();
        let caller_address = Helpers.to_uint256(current_address);
        let stack: model.Stack* = Stack.push(self=ctx.stack, element=caller_address);

        // Update the execution context.
        // Update context stack.
        let ctx = ExecutionContext.update_stack(self=ctx, new_stack=stack);
        // Increment gas used.
        let ctx = ExecutionContext.increment_gas_used(self=ctx, inc_value=GAS_COST_CALLER);
        return ctx;
    }

    // @notice CALLVALUE operation.
    // @dev Get deposited value by the instruction/transaction responsible for this execution.
    // @custom:since Frontier
    // @custom:group Environmental Information
    // @custom:gas 2
    // @custom:stack_consumed_elements 0
    // @custom:stack_produced_elements 1
    // @return The pointer to the updated execution context.
    func exec_callvalue{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        let uint256_value: Uint256 = Helpers.to_uint256(ctx.call_context.value);
        let stack: model.Stack* = Stack.push(ctx.stack, uint256_value);

        // Update the execution context.
        // Update context stack.
        let ctx = ExecutionContext.update_stack(ctx, stack);
        // Increment gas used.
        let ctx = ExecutionContext.increment_gas_used(ctx, GAS_COST_CALLVALUE);
        return ctx;
    }

    // @notice CALLDATALOAD operation.
    // @dev Push a word from the calldata onto the stack.
    // @custom:since Frontier
    // @custom:group Environmental Information
    // @custom:gas 3
    // @custom:stack_consumed_elements 1
    // @custom:stack_produced_elements 1
    // @param ctx The pointer to the execution context
    // @return The pointer to the updated execution context.
    func exec_calldataload{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        alloc_locals;

        let stack = ctx.stack;

        // Stack input:
        // 0 - offset: calldata offset of the word we read (32 byte steps).
        let (stack, calldata_offset) = Stack.pop(stack);

        let (sliced_calldata: felt*) = alloc();

        let calldata: felt* = ctx.call_context.calldata;
        let calldata_len: felt = ctx.call_context.calldata_len;

        // read calldata at offset
        let stack_element: Uint256 = get_uint256_in_array(
            offset=calldata_offset.low, code_len=calldata_len, code=calldata, len=32
        );

        // Push CallData word onto stack
        let stack: model.Stack* = Stack.push(self=stack, element=stack_element);

        // Update context stack.
        let ctx = ExecutionContext.update_stack(self=ctx, new_stack=stack);
        // Increment gas used.
        let ctx = ExecutionContext.increment_gas_used(self=ctx, inc_value=GAS_COST_CALLDATALOAD);
        return ctx;
    }

    // @notice CALLDATASIZE operation.
    // @dev Get the size of return data.
    // @custom:since Frontier
    // @custom:group Environmental Information
    // @custom:gas 2
    // @custom:stack_consumed_elements 0
    // @custom:stack_produced_elements 1
    // @param ctx The pointer to the execution context
    // @return The pointer to the updated execution context.
    func exec_calldatasize{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        let calldata_size = Helpers.to_uint256(ctx.call_context.original_calldata_len);
        let stack: model.Stack* = Stack.push(ctx.stack, calldata_size);

        // Update the execution context.
        // Update context stack.
        let ctx = ExecutionContext.update_stack(ctx, stack);
        // Increment gas used.
        let ctx = ExecutionContext.increment_gas_used(ctx, GAS_COST_CALLDATASIZE);
        return ctx;
    }

    // @notice CALLDATACOPY operation
    // @dev Save word to memory.
    // @custom:since Frontier
    // @custom:group Stack Memory Storage and Flow operations.
    // @custom:gas 3
    // @custom:stack_consumed_elements 3
    // @custom:stack_produced_elements 0
    // @param ctx The pointer to the execution context
    // @return Updated execution context.
    func exec_calldatacopy{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        alloc_locals;
        let (local sliced_calldata: felt*) = alloc();
        let stack = ctx.stack;

        // Stack input:
        // 0 - offset: memory offset of the work we save.
        // 1 - calldata_offset: offset for calldata from where data will be copied.
        // 2 - element_len: bytes length of the copied calldata.
        let (stack, popped) = Stack.pop_n(self=stack, n=3);
        let offset = popped[2];
        let calldata_offset = popped[1];
        let element_len = popped[0];

        let calldata: felt* = ctx.call_context.calldata;
        let calldata_len: felt = ctx.call_context.calldata_len;

        // Get calldata slice from calldata_offset to element_len
        slice_bytes_loop_translator(
            code_offset=calldata_offset.low,
            code_len=calldata_len,
            code=calldata,
            new_array_len=element_len.low - 1,
            new_array=sliced_calldata,
        );

        // Write caldata slice to memory at offset
        let memory: model.Memory* = Memory.store_n(
            self=ctx.memory, element_len=element_len.low, element=sliced_calldata, offset=offset.low
        );

        // Update context memory.
        let ctx = ExecutionContext.update_memory(self=ctx, new_memory=memory);
        // Update context stack.
        let ctx = ExecutionContext.update_stack(self=ctx, new_stack=stack);
        // Increment gas used.
        let ctx = ExecutionContext.increment_gas_used(self=ctx, inc_value=GAS_COST_CALLDATACOPY);
        return ctx;
    }

    // @notice CODESIZE operation.
    // @dev Get size of bytecode running in current environment.
    // @custom:since Frontier
    // @custom:group Environmental Information
    // @custom:gas 3
    // @custom:stack_consumed_elements 0
    // @custom:stack_produced_elements 1
    // @param ctx The pointer to the execution context
    // @return The pointer to the updated execution context.
    func exec_codesize{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        // Get the bytecode size.
        let code_size = Helpers.to_uint256(ctx.call_context.original_bytecode_len);

        %{
            import logging
            logging.info("CODESIZE DATA")
            logging.info(ids.code_size.low)
            logging.info(ids.code_size.high)
            logging.info(ids.ctx.call_context.original_bytecode_len)
        %}
        let stack: model.Stack* = Stack.push(self=ctx.stack, element=code_size);

        // Update the execution context.
        // Update context stack.
        let ctx = ExecutionContext.update_stack(self=ctx, new_stack=stack);
        // Increment gas used.
        let ctx = ExecutionContext.increment_gas_used(self=ctx, inc_value=GAS_COST_CODESIZE);
        return ctx;
    }

    // @notice CODECOPY (0x39) operation.
    // @dev Copies slice of bytecode to memory
    // @custom:since Frontier
    // @custom:group Environmental Information
    // @custom:gas 3
    // @custom:stack_consumed_elements 3
    // @custom:stack_produced_elements 0
    // @param ctx The pointer to the execution context
    // @return The pointer to the updated execution context.
    func exec_codecopy{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        alloc_locals;

        let stack = ctx.stack;
        let (local sliced_code: felt*) = alloc();

        // Stack input:
        // 0 - offset: memory offset of the work we save.
        // 1 - code_offset: offset for bytecode from where data will be copied.
        // 2 - element_len: bytes length of the copied bytecode.
        let (stack, popped) = Stack.pop_n(self=stack, n=3);
        let offset = popped[2];
        let code_offset = popped[1];
        let element_len = popped[0];

        // Get bytecode slice from code_offset to element_len
        let bytecode: felt* = ctx.call_context.bytecode;
        let bytecode_len: felt = ctx.call_context.bytecode_len;

        %{
            import logging
            logging.info("CODE COPY DATA")
            logging.info("OFFSET")
            logging.info(ids.offset.low)
            logging.info("CODE OFFSET")
            logging.info(ids.code_offset.low)
            logging.info("ELEMENT_LEN")
            logging.info(ids.element_len.low)

        %}

        slice_bytes_loop_translator(
            code_offset=code_offset.low,
            code_len=bytecode_len,
            code=bytecode,
            new_array_len=element_len.low - 1,
            new_array=sliced_code,
        );

        // Write bytecode slice to memory at offset
        let memory: model.Memory* = Memory.store_n(
            self=ctx.memory, element_len=element_len.low, element=sliced_code, offset=offset.low
        );

        // Update context memory.
        let ctx = ExecutionContext.update_memory(ctx, memory);
        // Update context stack.
        let ctx = ExecutionContext.update_stack(ctx, stack);
        // Increment gas used.
        let ctx = ExecutionContext.increment_gas_used(ctx, GAS_COST_CODECOPY);
        return ctx;
    }

    // @notice RETURNDATASIZE operation.
    // @dev Get the size of return data.
    // @custom:since Frontier
    // @custom:group Environmental Information
    // @custom:gas 2
    // @custom:stack_consumed_elements 0
    // @custom:stack_produced_elements 1
    // @param ctx The pointer to the execution context
    // @return The pointer to the updated execution context.
    func exec_returndatasize{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        // Get return data size.
        let return_data_size = Helpers.to_uint256(ctx.return_data_len);
        let stack: model.Stack* = Stack.push(self=ctx.stack, element=return_data_size);

        // Update the execution context.
        // Update context stack.
        let ctx = ExecutionContext.update_stack(self=ctx, new_stack=stack);
        // Increment gas used.
        let ctx = ExecutionContext.increment_gas_used(self=ctx, inc_value=GAS_COST_RETURNDATASIZE);
        return ctx;
    }

    // @notice RETURNDATACOPY operation
    // @dev Save word to memory.
    // @custom:since Frontier
    // @custom:group Stack Memory Storage and Flow operations.
    // @custom:gas 3
    // @custom:stack_consumed_elements 3
    // @custom:stack_produced_elements 0
    // @param ctx The pointer to the execution context
    // @return Updated execution context.
    func exec_returndatacopy{
        syscall_ptr: felt*,
        pedersen_ptr: HashBuiltin*,
        range_check_ptr,
        bitwise_ptr: BitwiseBuiltin*,
    }(ctx: model.ExecutionContext*) -> model.ExecutionContext* {
        alloc_locals;

        let stack = ctx.stack;

        // Stack input:
        // 0 - offset: memory offset of the work we save.
        // 1 - code_offset: offset for bytecode from where data will be copied.
        // 2 - element_len: bytes length of the copied bytecode.
        let (stack, popped) = Stack.pop_n(self=stack, n=3);
        let offset = popped[2];
        let return_data_offset = popped[1];
        let element_len = popped[0];

        let return_data: felt* = ctx.return_data;
        let return_data_len: felt = ctx.return_data_len;

        let sliced_return_data: felt* = Helpers.slice_data(
            data_len=return_data_len,
            data=return_data,
            data_offset=return_data_offset.low,
            slice_len=element_len.low,
        );

        let memory: model.Memory* = Memory.store_n(
            self=ctx.memory,
            element_len=element_len.low,
            element=sliced_return_data,
            offset=offset.low,
        );

        // Update context memory.
        let ctx = ExecutionContext.update_memory(self=ctx, new_memory=memory);
        // Update context stack.
        let ctx = ExecutionContext.update_stack(self=ctx, new_stack=stack);
        // Increment gas used.
        let ctx = ExecutionContext.increment_gas_used(ctx, GAS_COST_CALLDATACOPY);
        return ctx;
    }
}
