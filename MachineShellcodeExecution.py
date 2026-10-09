# Phase 3, Day 196: Python Fundamentals - Raw x86-64 Shellcode Execution
import ctypes
import mmap
import sys

print("--- Booting x86-64 Machine Code Injection Engine ---")

# 1. The Raw CPU Instructions (Shellcode)
# This is NOT Python bytecode. This is physical x86-64 Assembly Language.
# Assembly Translation:
#   mov eax, 42   (Move the integer 42 into the CPU's primary return register)
#   ret           (Return execution back to the caller)
x86_machine_code = b'\xb8\x2a\x00\x00\x00\xc3'

print(f"  [Payload] Hexadecimal Shellcode: {x86_machine_code.hex()}")

# --- Execution Environment ---

# 2. Allocate an Executable Memory Block via the Operating System
print("  [System] Requesting PROT_EXEC memory block from the OS kernel...")

# Note: Memory protection flags differ slightly between Windows and Unix
if sys.platform.startswith('win'):
    # Windows Implementation
    memory_buffer = mmap.mmap(-1, len(x86_machine_code), access=mmap.ACCESS_WRITE)
    # We must explicitly use VirtualProtect via ctypes to make it executable on Windows
    ctypes.windll.kernel32.VirtualProtect(
        ctypes.c_void_p(memory_buffer.fileno() if hasattr(memory_buffer, 'fileno') else id(memory_buffer)), 
        len(x86_machine_code), 
        0x40, # PAGE_EXECUTE_READWRITE
        ctypes.byref(ctypes.c_ulong(0))
    )
else:
    # Linux/Mac Implementation
    memory_buffer = mmap.mmap(-1, len(x86_machine_code), 
                              flags=mmap.MAP_SHARED | mmap.MAP_ANONYMOUS,
                              prot=mmap.PROT_WRITE | mmap.PROT_READ | mmap.PROT_EXEC)

# 3. Inject the Machine Code into the Executable RAM
print("  [System] Injecting hex bytes into physical RAM...")
memory_buffer.write(x86_machine_code)

# 4. Cast the raw memory address to a C-Function Signature using ctypes
print("  [System] Casting memory address to CFUNCTYPE...")
# We tell ctypes: "Treat this raw memory address as a function that takes 0 arguments and returns an int32"
buffer_address = ctypes.addressof(ctypes.c_void_p.from_buffer(memory_buffer))
C_Function_Signature = ctypes.CFUNCTYPE(ctypes.c_int32)

# Create the callable Python object that points to the CPU shellcode
hardware_level_function = C_Function_Signature(buffer_address)

# 5. Execute the Shellcode
print("\n--- Executing Hardware-Level Call ---")
print("Bypassing Python Interpreter...")

# The CPU physically executes our hex bytes and returns the value
result = hardware_level_function()

print(f"\nCRITICAL RESULT: CPU executed the shellcode and returned -> {result}")
print("Status: Python fundamentals verified. Python interpreter mathematically bypassed via raw executable memory injection.")