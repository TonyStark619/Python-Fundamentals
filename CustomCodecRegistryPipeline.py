# Phase 3, Master Day 223: Python Fundamentals - CPython Codec Registry & Error Trap Injection
import codecs
from typing import Tuple

print("--- Booting CPython Custom Codec & Wire-Fault Registry Engine ---")

CODEC_NAME = "hermetic-wire"
ERROR_HANDLER_NAME = "quarantine_corrupt_byte"
MAGIC_HEADER = b"\xAA\x55"


# 1. Custom C-Registry Error Handler Callback
def quarantine_fault_handler(error: UnicodeError) -> Tuple[str, int]:
    """
    Invoked automatically by the CPython codec kernel whenever a byte violates protocol rules.
    Returns (replacement_string, next_byte_index_to_resume).
    """
    if isinstance(error, UnicodeDecodeError):
        bad_byte = error.object[error.start]
        print(
            f"    -> [Codec Fault Trap] Corrupted wire byte {hex(bad_byte)} isolated "
            f"at index {error.start} ({error.reason}). Injecting quarantine marker..."
        )
        # Replace the corrupted byte with a visible marker and advance the cursor by 1 byte
        return ("\uFFFD[QUARANTINED]", error.start + 1)
    raise error


# 2. Custom Stateless Encoder & Decoder Functions
def hermetic_encode(input_str: str, errors: str = "strict") -> Tuple[bytes, int]:
    """
    Transcodes a Python string into a framed, rolling-key XOR binary packet.
    """
    raw_utf8 = input_str.encode("utf-8", errors)
    out_buffer = bytearray(MAGIC_HEADER)

    rolling_key = 0x5A
    for b in raw_utf8:
        cipher_byte = (b ^ rolling_key) & 0x7F  # Keep MSB 0 for valid wire parity
        out_buffer.append(cipher_byte)
        rolling_key = (rolling_key + 13) & 0x7F

    return (bytes(out_buffer), len(input_str))


def hermetic_decode(input_bytes: bytes, errors: str = "strict") -> Tuple[str, int]:
    """
    Validates frame headers, reverses rolling-XOR obfuscation, and triggers custom fault traps
    if high-bit wire corruption (MSB == 1) is detected in the payload.
    """
    raw_view = memoryview(input_bytes)
    if len(raw_view) < 2 or bytes(raw_view[:2]) != MAGIC_HEADER:
        raise ValueError("CRITICAL WIRE FAULT: Missing 0xAA55 Hermetic Frame Header.")

    decoded_chars = []
    rolling_key = 0x5A
    idx = 2

    while idx < len(raw_view):
        wire_byte = raw_view[idx]

        # Protocol Invariant: Payload bytes must never have the 8th bit (0x80) set
        if wire_byte & 0x80:
            exc = UnicodeDecodeError(
                CODEC_NAME,
                bytes(raw_view),
                idx,
                idx + 1,
                "High-bit parity violation detected on wire",
            )
            if errors == "strict":
                raise exc
            # Trigger the registered CPython error handler dynamically
            handler = codecs.lookup_error(errors)
            replacement, next_idx = handler(exc)
            decoded_chars.append(replacement)
            idx = next_idx
            rolling_key = (rolling_key + 13) & 0x7F
            continue

        clean_byte = (wire_byte ^ rolling_key) & 0x7F
        decoded_chars.append(chr(clean_byte))
        rolling_key = (rolling_key + 13) & 0x7F
        idx += 1

    return ("".join(decoded_chars), len(raw_view))


# 3. Codec Search Function for CPython's _PyCodec_Lookup Registry
def custom_codec_search_function(encoding_name: str):
    if encoding_name.lower().replace("_", "-") == CODEC_NAME:
        return codecs.CodecInfo(
            name=CODEC_NAME,
            encode=hermetic_encode,
            decode=hermetic_decode,
        )
    return None


# --- Execution Environment ---

print("  [System] Mounting custom codec and fault trap into CPython Registry...")
codecs.register(custom_codec_search_function)
codecs.register_error(ERROR_HANDLER_NAME, quarantine_fault_handler)

print("\n--- Diagnostic 1: Native str.encode() & bytes.decode() Transcoding ---")
secret_command = "AUTH_NODE:GUWAHATI_CLUSTER_09"

# Notice we call our custom binary protocol directly on a native Python string!
wire_packet: bytes = secret_command.encode("hermetic-wire")
print(f"  → Original String   : {secret_command}")
print(f"  → Framed Wire Hex   : {wire_packet.hex()}")

recovered_command: str = wire_packet.decode("hermetic-wire")
print(f"  → Decoded String    : {recovered_command}")

print("\n--- Diagnostic 2: Injecting Bit-Flip Corruption into Wire Packet ---")
corrupted_packet = bytearray(wire_packet)
# Flip the high parity bit at byte index 7 to simulate cosmic-ray / electromagnetic noise
corrupted_packet[7] |= 0x80

sanitized_output = bytes(corrupted_packet).decode(
    "hermetic-wire", errors="quarantine_corrupt_byte"
)
print(f"  → Sanitized Stream  : {sanitized_output}")

print("\nStatus: Python fundamentals verified. Native encode/decode pipelines extended via CPython CodecInfo and fault-trap registries.")