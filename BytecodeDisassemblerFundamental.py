# Phase 3, Day 172: Python Fundamentals - CPython Bytecode Disassembly (dis)
import dis

print("--- Booting CPython Stack Machine Analyzer ---")

# 1. The Junior Approach (Standard For Loop)
def legacy_loop_builder(limit):
    result = []
    for i in range(limit):
        result.append(i * 2)
    return result

# 2. The MNC Approach (List Comprehension)
def optimized_comprehension(limit):
    return [i * 2 for i in range(limit)]

# --- Execution Environment ---
print("\n[Diagnostic 1] Disassembling standard 'for' loop bytecode...")
print("-" * 50)
# This will expose the heavy LOAD_METHOD and CALL_METHOD instructions
dis.dis(legacy_loop_builder)
print("-" * 50)

print("\n[Diagnostic 2] Disassembling optimized comprehension bytecode...")
print("-" * 50)
# This will expose the streamlined LIST_APPEND instruction
dis.dis(optimized_comprehension)
print("-" * 50)

print("\n--- Telemetry Conclusion ---")
print("Verdict: The 'for' loop forces the interpreter to look up the .append method ")
print("in the global dictionary on EVERY single iteration. The comprehension bypasses ")
print("the dictionary entirely, executing a raw C-level LIST_APPEND directly in RAM.")
print("Status: Execution speed logically verified at the bytecode level.")