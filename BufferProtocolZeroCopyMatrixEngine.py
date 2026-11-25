# Phase 3, Master Day 241: Python Fundamentals - PEP 3118 Buffer Protocol, memoryview.cast & Export Locks
import struct

print("--- Booting CPython PEP 3118 Zero-Copy Buffer & Strided Matrix Engine ---")

ROWS, COLS = 3, 4
INT32_SIZE = struct.calcsize("i")
TOTAL_BYTES = ROWS * COLS * INT32_SIZE

# 1. Allocate a single contiguous raw memory block on the heap (48 bytes on standard 64-bit systems)
raw_arena = bytearray(TOTAL_BYTES)
print(f"  [Arena] Allocated single flat bytearray of {len(raw_arena)} bytes at {hex(id(raw_arena))}")

# 2. Acquire a PEP 3118 Py_buffer view and cast it in-place into a 2D (3 x 4) int32 matrix
base_view = memoryview(raw_arena)
matrix_view = base_view.cast("i", shape=[ROWS, COLS])

print("\n--- Diagnostic 1: Inspecting PEP 3118 Py_buffer Stride & Shape Metadata ---")
print(f"  → Format / Itemsize : '{matrix_view.format}' ({matrix_view.itemsize} bytes per element)")
print(f"  → Dimensions / Shape: ndim={matrix_view.ndim}, shape={matrix_view.shape}")
print(f"  → Byte Strides      : {matrix_view.strides} (Jump {matrix_view.strides[0]}B per row, {matrix_view.strides[1]}B per col)")
print(f"  → C-Contiguous?     : {matrix_view.c_contiguous}")

print("\n--- Diagnostic 2: Zero-Copy Bi-Directional Mutation Across Views ---")
# Populate the 2D matrix directly through tuple indexing (writes straight into raw_arena!)
for r in range(ROWS):
    for c in range(COLS):
        matrix_view[r, c] = (r + 1) * 100 + c

# Mutate cell [1, 2] to a distinct hexadecimal pattern: 0x01020304 (16,909,060)
matrix_view[1, 2] = 0x01020304

target_byte_offset = 1 * matrix_view.strides[0] + 2 * matrix_view.strides[1]
raw_slice_hex = raw_arena[target_byte_offset : target_byte_offset + INT32_SIZE].hex().upper()

print(f"  → Matrix Row 1 Snapshot        : {matrix_view.tolist()[1]}")
print(f"  → Backing bytearray[{target_byte_offset}:{target_byte_offset + INT32_SIZE}] Hex : 0x{raw_slice_hex} (Zero-copy write verified!)")

# Simultaneous cross-type aliasing: view the exact same 48 bytes as 6 IEEE-754 float64 values!
float64_alias = base_view.cast("d")
float64_alias[0] = 3.141592653589793
print(f"  → Float64 Alias [0] Written    : {float64_alias[0]} (Reinterpreting bytes 0..7 in-place!)")
print(f"  → Resulting Int32 [0,0] & [0,1]: ({matrix_view[0, 0]}, {matrix_view[0, 1]}) (Live IEEE-754 bit overlay!)")

print("\n--- Diagnostic 3: Enforcing C-Level Buffer Export Resize Lock (BufferError) ---")
try:
    # Attempting to reallocate raw_arena while Py_buffer views hold raw C pointers MUST fail!
    raw_arena.extend(b"\xFF\xFF")
except BufferError as exc:
    print(f"  → [C-Pointer Safety Lock Triggered] Resize blocked: {exc}")

# Explicitly release every exported Py_buffer handle to drop export count to 0
float64_alias.release()
matrix_view.release()
base_view.release()

# Now that zero external C pointers reference raw_arena, reallocation succeeds immediately!
raw_arena.extend(b"\xAA\xBB")
print(f"  → Post-.release() Resize Succeeded! New bytearray length = {len(raw_arena)} bytes")

print(
    "\nStatus: Python fundamentals verified. Multi-dimensional strided views and pointer-safe buffer locks executed with zero memory copies."
)