# Phase 3, Day 171: Python Fundamentals - Raw Memory Hacking (ctypes)
import ctypes
import sys

print("--- Booting Python C-Level Memory Override ---")

# 1. Define an immutable string
# We must use a short string so it doesn't get interned/cached globally in unexpected ways
original_string = "FAIL"
print(f"Original String: '{original_string}'")

# 2. Extract the absolute memory address of the string object
address = id(original_string)
print(f"Memory Address of Object: {hex(address)}")

# 3. Understand Python's internal String structure (PyASCIIObject)
# In Python 3, a string object has a header. 
# The actual character data usually starts roughly 48 bytes after the base address (varies by OS/architecture).
# sys.getsizeof() helps estimate this overhead.
offset = sys.getsizeof("") 

# 4. Create a C-level pointer to the exact byte where the characters start
pointer = (ctypes.c_char * 4).from_address(address + offset)

# 5. Overwrite the immutable memory directly
print("\n[System] Bypassing interpreter protections. Injecting raw bytes...")
pointer[0] = b"P"
pointer[1] = b"A"
pointer[2] = b"S"
pointer[3] = b"S"

# 6. The Verdict
print(f"\nModified String: '{original_string}'")

if original_string == "PASS":
    print("CRITICAL RESULT: Immutable object successfully mutated via raw memory injection.")
else:
    print("Result: Memory offset incorrect for this specific OS architecture.")
    
print("\nStatus: Python fundamentals verified. C-level memory access achieved.")