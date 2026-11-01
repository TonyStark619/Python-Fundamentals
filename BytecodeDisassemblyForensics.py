# Phase 3, Master Day 219: Python Fundamentals - CPython Bytecode Disassembly (dis)
import dis

print("--- Booting CPython Bytecode Forensics Engine ---")

# 1. The Target Function
# We will mathematically prove why X = X * 2 is executed differently than X *= 2
def enterprise_computation(x):
    # Standard assignment
    y = x * 2
    
    # In-place assignment
    y *= 2
    
    return y

# 2. Extracting and Analyzing the Raw Execution Stack
def execute_bytecode_sweep(target_function):
    print(f"  [System] Disassembling memory space for: '{target_function.__name__}()'")
    
    # The 'dis.get_instructions' generator allows us to dynamically analyze the bytecode
    # instead of just printing it to the console.
    bytecode_instructions = dis.get_instructions(target_function)
    
    print("\n  [Execution Stack Mapping]")
    print(f"  {'Line':<6} | {'Opcode Name':<20} | {'Arg Val':<15} | {'Instruction Description'}")
    print("-" * 75)
    
    for instruction in bytecode_instructions:
        line_num = instruction.starts_line if instruction.starts_line else ""
        
        # Determine the description based on the specific CPython opcode
        desc = ""
        if "LOAD_FAST" in instruction.opname:
            desc = "Pushes a local variable onto the execution stack."
        elif "LOAD_CONST" in instruction.opname:
            desc = "Pushes a constant (like an integer) onto the stack."
        elif "BINARY_MULTIPLY" in instruction.opname:
            desc = "Pops two stack items, multiplies them, pushes result."
        elif "INPLACE_MULTIPLY" in instruction.opname:
            desc = "Modifies the variable directly in memory (Zero-copy optimization)."
        elif "STORE_FAST" in instruction.opname:
            desc = "Pops the stack and saves it back to a local variable."
            
        print(f"  {line_num:<6} | {instruction.opname:<20} | {str(instruction.argval):<15} | {desc}")

# --- Execution Environment ---

print("\n[System] Initiating Bytecode Extraction Protocol...\n")
execute_bytecode_sweep(enterprise_computation)

print("\n--- Diagnostic Analysis ---")
print("  -> Notice that 'y = x * 2' uses BINARY_MULTIPLY (Creates a new object in RAM).")
print("  -> Notice that 'y *= 2' uses INPLACE_MULTIPLY (Mutates the object if possible).")

print("\nStatus: Python fundamentals verified. Abstract syntax successfully deconstructed into raw CPython stack-machine opcodes.")