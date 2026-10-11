# Phase 3, Day 199: Python Fundamentals - Raw Bytecode Opcode Forging (types.CodeType)
import types
import opcode

print("--- Booting CPython Raw Opcode Forger ---")

# 1. We dynamically look up the CPython opcode integers for the current interpreter version
LOAD_FAST = opcode.opmap['LOAD_FAST']
BINARY_MULTIPLY = opcode.opmap['BINARY_MULTIPLY']
RETURN_VALUE = opcode.opmap['RETURN_VALUE']

print("  [System] Target Opcodes Acquired:")
print(f"    -> LOAD_FAST: {LOAD_FAST}")
print(f"    -> BINARY_MULTIPLY: {BINARY_MULTIPLY}")
print(f"    -> RETURN_VALUE: {RETURN_VALUE}")

# 2. We construct the raw byte-stream for the logic: return x * y
# Every instruction is 2 bytes: (opcode, argument_index)
raw_bytecode_payload = bytes([
    LOAD_FAST, 0,        # Load local variable at index 0 ('x') onto the stack
    LOAD_FAST, 1,        # Load local variable at index 1 ('y') onto the stack
    BINARY_MULTIPLY, 0,  # Pop top two elements, multiply them, push result to stack (arg is 0)
    RETURN_VALUE, 0      # Pop top element and return it
])

print(f"\n  [System] Hexadecimal Bytecode Payload Assembled: {raw_bytecode_payload.hex()}")

# 3. Create an empty dummy function to act as our shell
def empty_shell(x, y):
    pass

print(f"  [System] Empty Shell initialized. Current output: {empty_shell(5, 5)}")

# 4. THE MAGIC: We inject the raw byte-stream directly into the function's Code Object
print("  [System] Injecting forged bytecode into the shell's memory space...")

original_code = empty_shell.__code__

# We construct a new CodeType object, perfectly copying the shell's metadata, 
# but completely replacing the 'co_code' execution payload with our raw hex bytes.
forged_code = original_code.replace(co_code=raw_bytecode_payload)

# Overwrite the shell's brain
empty_shell.__code__ = forged_code

# --- Execution Environment ---
print("\n--- Executing Forged Hexadecimal Logic ---")

val1, val2 = 12, 10
print(f"Passing ({val1}, {val2}) into the mutated shell...")

# The Python Interpreter natively executes our injected opcodes
result = empty_shell(val1, val2)

print(f"\nCRITICAL RESULT: Hardware-level multiplication executed successfully -> {result}")
print("Status: Python fundamentals verified. AST and Compiler completely bypassed via manual CodeType bytecode integer packing.")