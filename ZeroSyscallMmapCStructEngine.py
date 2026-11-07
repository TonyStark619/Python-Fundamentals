# Phase 3, Master Day 225: Python Fundamentals - Zero-Syscall Page-Cache C-Struct Mapping
import ctypes
import mmap
import os
import tempfile

print("--- Booting CPython Zero-Syscall mmap + ctypes.Structure Engine ---")


# 1. Define a Strict 1-Byte Aligned Hardware/IPC C-Structure (Total: 24 Bytes)
classSharedTelemetryHeader(ctypes.Structure):
    """
    _pack_ = 1 instructs the C ABI to disable compiler padding bytes,
    guaranteeing deterministic byte offsets across C, Rust, and Python processes.
    """
    _pack_ = 1
    _fields_ = [
        ("magic_signature", ctypes.c_uint32),  # 4 bytes (Offset 0)
        ("sequence_id", ctypes.c_uint64),      # 8 bytes (Offset 4)
        ("cpu_load_Permille", ctypes.c_uint16),# 2 bytes (Offset 12)
        ("status_flags", ctypes.c_uint8),      # 1 byte  (Offset 14)
        ("node_tag", ctypes.c_char * 9),       # 9 bytes (Offset 15..23)
    ]


STRUCT_BYTE_SIZE = ctypes.sizeof(classSharedTelemetryHeader)
print(f"  [ABI Layout] Packed C-Structure Size Verified: {STRUCT_BYTE_SIZE} bytes")


# --- Execution Environment ---

# Create a temporary physical backing file on disk
fd, temp_filepath = tempfile.mkstemp(prefix="ipc_telemetry_", suffix=".shm")
os.close(fd)

try:
    # Pre-allocate the exact 24-byte physical file boundary
    with open(temp_filepath, "wb") as f:
        f.write(b"\x00" * STRUCT_BYTE_SIZE)

    # Open the file for Read/Write and map it into the OS Virtual Memory Page Cache
    with open(temp_filepath, "r+b") as backing_file:
        with mmap.mmap(
            backing_file.fileno(),
            length=STRUCT_BYTE_SIZE,
            access=mmap.ACCESS_WRITE,
        ) as kernel_page_map:

            print("\n--- Diagnostic 1: Zero-Copy C-Struct Overlay via .from_buffer() ---")
            # Overlay the C-Struct directly onto the OS memory-mapped page buffer
            live_header = classSharedTelemetryHeader.from_buffer(kernel_page_map)

            # Mutating these attributes writes directly to the OS Page Cache in RAM
            # without calling file.write() or struct.pack()!
            live_header.magic_signature = 0xCAFEBABE
            live_header.sequence_id = 900_000_001
            live_header.cpu_load_Permille = 845  # 84.5% load
            live_header.status_flags = 0b0000_0101
            live_header.node_tag = b"GHY_CORE1"

            print(f"  → Struct Written via RAM Pointer : magic={hex(live_header.magic_signature)}, seq={live_header.sequence_id}")
            print(f"  → Raw OS Page-Cache Hex Dump     : {kernel_page_map[:].hex()}")

            print("\n--- Diagnostic 2: Bi-Directional Hardware Byte Mutation ---")
            # Mutate byte offset 14 (status_flags) directly inside the raw mmap buffer
            kernel_page_map[14] = 0xFF

            # The C-Struct reflects the new byte immediately because they share the exact virtual address
            print(f"  → Direct mmap[14] Mutation       : 0xFF")
            print(f"  → Live C-Struct status_flags     : {hex(live_header.status_flags)}")

            # Delete the ctypes pointer reference before closing the underlying mmap
            del live_header
            kernel_page_map.flush()

    print("\n--- Diagnostic 3: Persisted Disk Verification ---")
    with open(temp_filepath, "rb") as verify_file:
        persisted_bytes = verify_file.read()
        readonly_struct = classSharedTelemetryHeader.from_buffer_copy(persisted_bytes)
        print(
            f"  → Recovered from Disk            : Node='{readonly_struct.node_tag.decode()}', "
            f"Seq={readonly_struct.sequence_id}, Flags={hex(readonly_struct.status_flags)}"
        )

finally:
    if os.path.exists(temp_filepath):
        os.remove(temp_filepath)

print("\nStatus: Python fundamentals verified. User-to-kernel I/O syscalls bypassed via mmap and ctypes.Structure.from_buffer().")