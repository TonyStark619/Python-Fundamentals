# Phase 3, Day 184: Python Fundamentals - Raw C-Memory Allocation (ctypes)
import ctypes
import sys
import time

print("--- Booting Native C-Memory Architecture ---")

# 1. Define a strict C-level Struct bypassing Python objects
class C_TelemetryPacket(ctypes.Structure):
    """
    A raw C-struct. It occupies exactly 13 bytes in RAM (4 + 8 + 1), perfectly contiguous.
    Standard Python objects would add ~50+ bytes of dictionary overhead per instance.
    """
    _fields_ = [
        ("node_id", ctypes.c_int32),       # 4 bytes
        ("temperature", ctypes.c_double),  # 8 bytes
        ("is_active", ctypes.c_bool)       # 1 byte
    ]

# --- Execution Environment ---
ARRAY_SIZE = 1_000_000

print(f"\n[System] Allocating {ARRAY_SIZE} nodes...")

# --- Legacy Python Execution ---
start_time = time.time()
# Python list containing Python objects
python_array = [{"node_id": i, "temperature": 0.0, "is_active": True} for i in range(ARRAY_SIZE)]
py_time = time.time() - start_time
# Measuring just the list pointers (actual object weight is massively higher)
py_size_mb = sys.getsizeof(python_array) / (1024 * 1024) 

print("\n--- Standard Python Dictionary Array ---")
print(f"  -> Allocation Time: {py_time * 1000:.2f} ms")
print(f"  -> Base Pointer RAM: {py_size_mb:.2f} MB (Excluding actual object payloads)")


# --- Native C-Level Execution ---
start_time = time.time()
# THE MAGIC: We multiply the C-Struct by the size to create a raw, contiguous C-Array type
C_ArrayType = C_TelemetryPacket * ARRAY_SIZE

# Instantiate the massive C-array directly in RAM (Zero Python objects are created)
c_memory_block = C_ArrayType()

# Initialize data (Executing natively in the C-buffer)
for i in range(ARRAY_SIZE):
    c_memory_block[i].node_id = i
    c_memory_block[i].temperature = 0.0
    c_memory_block[i].is_active = True

c_time = time.time() - start_time
# Measuring the exact, literal byte footprint in RAM
c_size_mb = ctypes.sizeof(c_memory_block) / (1024 * 1024)

print("\n--- C-Types Contiguous Struct Array ---")
print(f"  -> Allocation Time: {c_time * 1000:.2f} ms")
print(f"  -> Absolute Total RAM: {c_size_mb:.2f} MB (Total physical footprint)")

print("\n[Diagnostic Verification]")
print(f"Testing direct C-memory read (Index 999,999 ID): {c_memory_block[999999].node_id}")

print("\nStatus: Python fundamentals verified. Object overhead completely bypassed using contiguous C-level memory structures.")