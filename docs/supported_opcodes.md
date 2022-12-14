# Kakarot supported EVM opcodes ๐งช

This document describes the opcodes supported by Kakarot.

## Arithmetic operations

| Opcode Value | Opcode Name | Description                                      | Implemented |
| ------------ | ----------- | ------------------------------------------------ | ----------- |
| 0x01         | ADD         | Addition operation                               | โ           |
| 0x02         | MUL         | Multiplication operation                         | โ           |
| 0x03         | SUB         | Subtraction operation                            | โ           |
| 0x04         | DIV         | Integer division operation                       | โ           |
| 0x05         | SDIV        | Signed integer division operation (truncated)    | โ           |
| 0x06         | MOD         | Modulo remainder operation                       | โ           |
| 0x07         | SMOD        | Signed modulo remainder operation                | โ           |
| 0x08         | ADDMOD      | Modulo addition operation                        | โ           |
| 0x09         | MULMOD      | Modulo multiplication operation                  | โ           |
| 0x0a         | EXP         | Exponential operation                            | โ           |
| 0x0b         | SIGNEXTEND  | Extend length of two's complement signed integer | โ           |

## Comparison & bitwise logic operations

| Opcode Value | Opcode Name | Description                    | Implemented |
| ------------ | ----------- | ------------------------------ | ----------- |
| 0x10         | LT          | Less-than comparison           | โ           |
| 0x11         | GT          | Greater-than comparison        | โ           |
| 0x12         | SLT         | Signed less-than comparison    | โ           |
| 0x13         | SGT         | Signed greater-than comparison | โ           |
| 0x14         | EQ          | Equality comparison            | โ           |
| 0x15         | ISZERO      | Simple not operator            | โ           |
| 0x16         | AND         | Bitwise AND operation          | โ           |
| 0x17         | OR          | Bitwise OR operation           | โ           |
| 0x18         | XOR         | Bitwise XOR operation          | โ           |
| 0x19         | NOT         | Bitwise NOT operation          | โ           |
| 0x1a         | BYTE        | Retrieve single byte from word | โ           |
| 0x1b         | SHL         | Shift left                     | โ           |
| 0x1c         | SHR         | Logical shift right            | โ           |
| 0x1d         | SAR         | Arithmetic shift right         | โ           |

## SHA3

| Opcode Value | Opcode Name | Description             | Implemented |
| ------------ | ----------- | ----------------------- | ----------- |
| 0x20         | SHA3        | Compute Keccak-256 hash | โ           |

## Environmental Information

| Opcode Value | Opcode Name    | Description                                                                       | Implemented |
| ------------ | -------------- | --------------------------------------------------------------------------------- | ----------- |
| 0x30         | ADDRESS        | Get address of currently executing account                                        | โ           |
| 0x31         | BALANCE        | Get balance of the given account                                                  | โ           |
| 0x32         | ORIGIN         | Get execution origination address                                                 | โ           |
| 0x33         | CALLER         | Get caller address                                                                | โ           |
| 0x34         | CALLVALUE      | Get deposited value by the instruction/transaction responsible for this execution | โ           |
| 0x35         | CALLDATALOAD   | Get input data of current environment                                             | โ           |
| 0x36         | CALLDATASIZE   | Get size of input data in current environment                                     | โ           |
| 0x37         | CALLDATACOPY   | Copy input data in current environment to memory                                  | โ           |
| 0x38         | CODESIZE       | Get size of code running in current environment                                   | โ           |
| 0x39         | CODECOPY       | Copy code running in current environment to memory                                | โ           |
| 0x3a         | GASPRICE       | Get price of gas in current environment                                           | โ           |
| 0x3b         | EXTCODESIZE    | Get size of an account's code                                                     | โ           |
| 0x3c         | EXTCODECOPY    | Copy an account's code to memory                                                  | โ           |
| 0x3d         | RETURNDATASIZE | Get size of output data from the previous call from the current environment       | โ           |
| 0x3e         | RETURNDATACOPY | Copy output data from the previous call to memory                                 | โ           |
| 0x3f         | EXTCODEHASH    | Get the code hash of an account                                                   | โ           |

## Block Information

| Opcode Value | Opcode Name | Description                                                | Implemented |
| ------------ | ----------- | ---------------------------------------------------------- | ----------- |
| 0x40         | BLOCKHASH   | Get the hash of one of the 256 most recent complete blocks | โ           |
| 0x41         | COINBASE    | Get the block's beneficiary address                        | โ           |
| 0x42         | TIMESTAMP   | Get the block's timestamp                                  | โ           |
| 0x43         | NUMBER      | Get the block's number                                     | โ           |
| 0x44         | DIFFICULTY  | Get the block's difficulty                                 | โ           |
| 0x45         | GASLIMIT    | Get the block's gas limit                                  | โ           |
| 0x46         | CHAINID     | Get the chain ID                                           | โ           |
| 0x47         | SELFBALANCE | Get the balance of the current contract                    | โ           |
| 0x48         | BASEFEE     | Get the base fee of the current block                      | โ           |

## Stack, Memory, Storage and Flow Operations

| Opcode Value | Opcode Name | Description                                                                                        | Implemented |
| ------------ | ----------- | -------------------------------------------------------------------------------------------------- | ----------- |
| 0x50         | POP         | Remove item from stack                                                                             | โ           |
| 0x51         | MLOAD       | Load word from memory                                                                              | โ           |
| 0x52         | MSTORE      | Save word to memory                                                                                | โ           |
| 0x53         | MSTORE8     | Save byte to memory                                                                                | โ           |
| 0x54         | SLOAD       | Load word from storage                                                                             | โ           |
| 0x55         | SSTORE      | Save word to storage                                                                               | โ           |
| 0x56         | JUMP        | Alter the program counter                                                                          | โ           |
| 0x57         | JUMPI       | Conditionally alter the program counter                                                            | โ           |
| 0x58         | PC          | Get the value of the program counter prior to the increment                                        | โ           |
| 0x59         | MSIZE       | Get the size of active memory in bytes                                                             | โ           |
| 0x5a         | GAS         | Get the amount of available gas, including the corresponding reduction the amount of available gas | โ           |
| 0x5b         | JUMPDEST    | Mark a valid destination for jumps                                                                 | โ           |

## Push Operations

| Opcode Value | Opcode Name | Description                             | Implemented |
| ------------ | ----------- | --------------------------------------- | ----------- |
| 0x60         | PUSH1       | Place 1 byte item on stack              | โ           |
| 0x61         | PUSH2       | Place 2-byte item on stack              | โ           |
| 0x62         | PUSH3       | Place 3-byte item on stack              | โ           |
| 0x63         | PUSH4       | Place 4-byte item on stack              | โ           |
| 0x64         | PUSH5       | Place 5-byte item on stack              | โ           |
| 0x65         | PUSH6       | Place 6-byte item on stack              | โ           |
| 0x66         | PUSH7       | Place 7-byte item on stack              | โ           |
| 0x67         | PUSH8       | Place 8-byte item on stack              | โ           |
| 0x68         | PUSH9       | Place 9-byte item on stack              | โ           |
| 0x69         | PUSH10      | Place 10-byte item on stack             | โ           |
| 0x6a         | PUSH11      | Place 11-byte item on stack             | โ           |
| 0x6b         | PUSH12      | Place 12-byte item on stack             | โ           |
| 0x6c         | PUSH13      | Place 13-byte item on stack             | โ           |
| 0x6d         | PUSH14      | Place 14-byte item on stack             | โ           |
| 0x6e         | PUSH15      | Place 15-byte item on stack             | โ           |
| 0x6f         | PUSH16      | Place 16-byte item on stack             | โ           |
| 0x70         | PUSH17      | Place 17-byte item on stack             | โ           |
| 0x71         | PUSH18      | Place 18-byte item on stack             | โ           |
| 0x72         | PUSH19      | Place 19-byte item on stack             | โ           |
| 0x73         | PUSH20      | Place 20-byte item on stack             | โ           |
| 0x74         | PUSH21      | Place 21-byte item on stack             | โ           |
| 0x75         | PUSH22      | Place 22-byte item on stack             | โ           |
| 0x76         | PUSH23      | Place 23-byte item on stack             | โ           |
| 0x77         | PUSH24      | Place 24-byte item on stack             | โ           |
| 0x78         | PUSH25      | Place 25-byte item on stack             | โ           |
| 0x79         | PUSH26      | Place 26-byte item on stack             | โ           |
| 0x7a         | PUSH27      | Place 27-byte item on stack             | โ           |
| 0x7b         | PUSH28      | Place 28-byte item on stack             | โ           |
| 0x7c         | PUSH29      | Place 29-byte item on stack             | โ           |
| 0x7d         | PUSH30      | Place 30-byte item on stack             | โ           |
| 0x7e         | PUSH31      | Place 31-byte item on stack             | โ           |
| 0x7f         | PUSH32      | Place 32-byte (full word) item on stack | โ           |

## Duplication Operations

| Opcode Value | Opcode Name | Description               | Implemented |
| ------------ | ----------- | ------------------------- | ----------- |
| 0x80         | DUP1        | Duplicate 1st stack item  | โ           |
| 0x81         | DUP2        | Duplicate 2nd stack item  | โ           |
| 0x82         | DUP3        | Duplicate 3rd stack item  | โ           |
| 0x83         | DUP4        | Duplicate 4th stack item  | โ           |
| 0x84         | DUP5        | Duplicate 5th stack item  | โ           |
| 0x85         | DUP6        | Duplicate 6th stack item  | โ           |
| 0x86         | DUP7        | Duplicate 7th stack item  | โ           |
| 0x87         | DUP8        | Duplicate 8th stack item  | โ           |
| 0x88         | DUP9        | Duplicate 9th stack item  | โ           |
| 0x89         | DUP10       | Duplicate 10th stack item | โ           |
| 0x8a         | DUP11       | Duplicate 11th stack item | โ           |
| 0x8b         | DUP12       | Duplicate 12th stack item | โ           |
| 0x8c         | DUP13       | Duplicate 13th stack item | โ           |
| 0x8d         | DUP14       | Duplicate 14th stack item | โ           |
| 0x8e         | DUP15       | Duplicate 15th stack item | โ           |
| 0x8f         | DUP16       | Duplicate 16th stack item | โ           |

## Exchange Operations

| Opcode Value | Opcode Name | Description                       | Implemented |
| ------------ | ----------- | --------------------------------- | ----------- |
| 0x90         | SWAP1       | Exchange 1st and 2nd stack items  | โ           |
| 0x91         | SWAP2       | Exchange 1st and 3rd stack items  | โ           |
| 0x92         | SWAP3       | Exchange 1st and 4th stack items  | โ           |
| 0x93         | SWAP4       | Exchange 1st and 5th stack items  | โ           |
| 0x94         | SWAP5       | Exchange 1st and 6th stack items  | โ           |
| 0x95         | SWAP6       | Exchange 1st and 7th stack items  | โ           |
| 0x96         | SWAP7       | Exchange 1st and 8th stack items  | โ           |
| 0x97         | SWAP8       | Exchange 1st and 9th stack items  | โ           |
| 0x98         | SWAP9       | Exchange 1st and 10th stack items | โ           |
| 0x99         | SWAP10      | Exchange 1st and 11th stack items | โ           |
| 0x9a         | SWAP11      | Exchange 1st and 12th stack items | โ           |
| 0x9b         | SWAP12      | Exchange 1st and 13th stack items | โ           |
| 0x9c         | SWAP13      | Exchange 1st and 14th stack items | โ           |
| 0x9d         | SWAP14      | Exchange 1st and 15th stack items | โ           |
| 0x9e         | SWAP15      | Exchange 1st and 16th stack items | โ           |
| 0x9f         | SWAP16      | Exchange 1st and 17th stack items | โ           |

## Logging Operations

| Opcode Value | Opcode Name | Description                         | Implemented |
| ------------ | ----------- | ----------------------------------- | ----------- |
| 0xa0         | LOG0        | Append log record with no topics    | โ           |
| 0xa1         | LOG1        | Append log record with one topic    | โ           |
| 0xa2         | LOG2        | Append log record with two topics   | โ           |
| 0xa3         | LOG3        | Append log record with three topics | โ           |
| 0xa4         | LOG4        | Append log record with four topics  | โ           |

## System Operations

| Opcode Value | Opcode Name  | Description                                                       | Implemented |
| ------------ | ------------ | ----------------------------------------------------------------- | ----------- |
| 0xf0         | CREATE       | Create a new account with associated code                         | โ           |
| 0xf1         | CALL         | Message-call into an account                                      | โ           |
| 0xf2         | CALLCODE     | Message-call into this account with alternative account's code    | โ           |
| 0xf3         | RETURN       | Halt execution returning output data                              | โ           |
| 0xf4         | DELEGATECALL | Message-call into this account with an alternative accountโs code | โ           |
| 0xf5         | CREATE2      | Create a new account with associated code                         | โ           |
| 0xfa         | STATICCALL   | Static message-call into an account                               | โ           |
| 0xfd         | REVERT       | Halt execution reverting state changes                            | โ           |
| 0xfe         | INVALID      | Designated invalid instruction                                    | โ           |
| 0xff         | SELFDESTRUCT | Halt execution and register account for later deletion            | โ           |
