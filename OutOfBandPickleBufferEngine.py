# Phase 3, Master Day 222: Python Fundamentals - Out-of-Band Serialization (PickleBuffer + copyreg)
import copyreg
import pickle
from typing import List

print("--- Booting CPython Protocol-5 Out-of-Band Serialization Engine ---")


class ZeroCopyTensorPacket:
    """
    Represents an enterprise tensor/frame object holding metadata and a contiguous memory buffer.
    """
    def __init__(self, tensor_id: str, shape: tuple, raw_buffer: memoryview):
        self.tensor_id = tensor_id
        self.shape = shape
        # Store as a zero-copy memoryview
        self.raw_buffer = memoryview(raw_buffer)


def reconstruct_tensor_packet(tensor_id: str, shape: tuple, buffer_obj: pickle.PickleBuffer) -> ZeroCopyTensorPacket:
    """
    Reconstruction hook called by CPython's unpickler.
    Receives the raw out-of-band memory buffer without duplicating bytes.
    """
    return ZeroCopyTensorPacket(tensor_id, shape, memoryview(buffer_obj))


def reduce_tensor_packet(packet: ZeroCopyTensorPacket):
    """
    Custom C-dispatch reducer registered via copyreg.
    Wraps the heavy payload in a PEP 574 PickleBuffer so Protocol 5 extracts it out-of-band.
    """
    print(f"    [copyreg Hook] Intercepted '{packet.tensor_id}'. Wrapping payload in PickleBuffer...")
    oob_buffer = pickle.PickleBuffer(packet.raw_buffer)
    return reconstruct_tensor_packet, (packet.tensor_id, packet.shape, oob_buffer)


# 1. Register the custom C-level dispatch rule in Python's global copyreg table
copyreg.pickle(ZeroCopyTensorPacket, reduce_tensor_packet)


# --- Execution Environment ---

# Allocate a 10 MB contiguous bytearray in physical RAM
PAYLOAD_SIZE = 10 * 1024 * 1024
physical_ram_block = bytearray(b"\x42" * PAYLOAD_SIZE)
original_packet = ZeroCopyTensorPacket("TENSOR_NODE_09", (1024, 10240), memoryview(physical_ram_block))

# List to capture out-of-band zero-copy memory buffers during serialization
out_of_band_buffers: List[pickle.PickleBuffer] = []

print("\n--- Diagnostic 1: Executing Protocol-5 Out-of-Band Serialization ---")
# buffer_callback intercepts every PickleBuffer and diverts it out of the main byte stream!
in_band_metadata_stream = pickle.dumps(
    original_packet,
    protocol=5,
    buffer_callback=out_of_band_buffers.append
)

print(f"  → Original Payload Size       : {PAYLOAD_SIZE:,} bytes (10.00 MB)")
print(f"  → In-Band Metadata Stream Size: {len(in_band_metadata_stream)} bytes (Zero payload bytes copied!)")
print(f"  → Out-of-Band Buffers Captured: {len(out_of_band_buffers)}")

print("\n--- Diagnostic 2: Verifying Zero-Copy Physical Memory Identity ---")
# Reconstruct the object by combining the tiny metadata stream with the out-of-band buffer pointers
reconstructed_packet: ZeroCopyTensorPacket = pickle.loads(
    in_band_metadata_stream,
    buffers=out_of_band_buffers
)

# Mutate a single byte in the original physical bytearray
physical_ram_block[0] = 0x99

# Because the entire pipeline was zero-copy, the reconstructed object sees the mutation immediately!
print(f"  → Mutated Byte at Original RAM[0]       : {hex(physical_ram_block[0])}")
print(f"  → Byte Read from Reconstructed Packet[0]: {hex(reconstructed_packet.raw_buffer[0])}")

if reconstructed_packet.raw_buffer[0] == 0x99:
    print("\nCRITICAL RESULT: 100% Zero-Copy verified. Reconstructed object shares the exact physical RAM address.")

print("Status: Python fundamentals verified. Serialization RAM bottlenecks eliminated via PEP 574 PickleBuffer and copyreg dispatch.")