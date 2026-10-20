# Phase 3, Day 209: Python Fundamentals - Native OS Library Hooking (ctypes)
import ctypes
import ctypes.util
import sys

print("--- Booting OS-Level Native C-Library Interceptor ---")

# 1. Locate the absolute physical file of the C Standard Library for the current Operating System
print("  [System] Scanning Operating System for native C libraries...")

if sys.platform == 'win32':
    # Windows uses the Microsoft C Runtime
    libc_name = ctypes.util.find_library('msvcrt')
else:
    # Linux, Mac, and Unix systems use the standard GNU/C library
    libc_name = ctypes.util.find_library('c')

if not libc_name:
    print("  [ALERT] OS Native C Library not found. Halting execution.")
    sys.exit(1)

print(f"  [System] Native Library Isolated: {libc_name}")

# 2. Mathematically load the physical OS binary into Python's memory space
libc = ctypes.CDLL(libc_name)
print("  [System] Hardware library successfully mounted into RAM.")

# --- Execution Environment ---

# 3. Hijacking native C 'printf' (Bypassing Python's print() function entirely)
print("\n--- Diagnostic 1: C-Level printf Execution ---")

# We must define the C-function signature so Python knows how to pack the memory
libc.printf.argtypes = [ctypes.c_char_p]
libc.printf.restype = ctypes.c_int

# We construct a strict C-style byte string (null-terminated automatically by ctypes)
c_string_payload = b"    -> [Hardware I/O] This text was rendered strictly by native C printf, bypassing sys.stdout!\n"

# Execute the OS-level function directly
bytes_written = libc.printf(c_string_payload)
print(f"    -> [Python I/O] C-Library confirmed {bytes_written} bytes were pushed to the physical terminal.")


# 4. Hijacking native C 'rand' and 'srand' (Bypassing Python's random module)
print("\n--- Diagnostic 2: Hardware Level Random Generation ---")

libc.srand.argtypes = [ctypes.c_uint]
libc.rand.argtypes = []
libc.rand.restype = ctypes.c_int

# Seed the C-level random generator with an arbitrary integer
SEED_VALUE = 42
libc.srand(SEED_VALUE)
print(f"  [Kernel] C-Library Random Engine seeded with {SEED_VALUE}.")

# Extract raw random integers directly from the OS C-runtime
val1 = libc.rand()
val2 = libc.rand()

print(f"  -> First OS Native Random Integer:  {val1}")
print(f"  -> Second OS Native Random Integer: {val2}")

print("\nStatus: Python fundamentals verified. Standard library bypassed and direct OS C-Runtime hardware functions executed.")