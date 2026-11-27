# Phase 3, Master Day 243: Python Fundamentals - C-Level Codec Registry & Custom Error Handlers (codecs)
import codecs
from typing import List, Optional, Tuple, Union

print("--- Booting CPython C-Level Codec Search Registry & Fault-Recovery Engine ---")

CODEC_NAME = "telemetry_xor_v1"
MAGIC_HEADER = b"\x54\x58"  # 'TX' framing signature
XOR_MASK = 0x5A

# Forensic log capturing every corrupt byte sequence intercepted mid-stream
CORRUPTION_AUDIT_LOG: List[str] = []


# 1. Custom Pluggable C-Decoder Error Handler (codecs.register_error)
def quarantine_corrupt_bytes_handler(exc: UnicodeError) -> Tuple[Union[str, bytes], int]:
    """
    Invoked directly by CPython's C decoder loop whenever a byte sequence violates UTF-8.
    Returns (replacement_str, resume_byte_index) so decoding continues without data loss!
    """
    if isinstance(exc, UnicodeDecodeError):
        bad_bytes = exc.object[exc.start : exc.end]
        hex_repr = bad_bytes.hex().upper()
        CORRUPTION_AUDIT_LOG.append(
            f"Offset [{exc.start}:{exc.end}] | Raw=0x{hex_repr} | Reason={exc.reason}"
        )
        return (f"<CORRUPT:0x{hex_repr}>", exc.end)

    if isinstance(exc, UnicodeEncodeError):
        bad_char = exc.object[exc.start : exc.start + 1]
        code_point = f"U+{ord(bad_char):04X}"
        CORRUPTION_AUDIT_LOG.append(
            f"CharIndex {exc.start} | CodePoint={code_point} | Reason={exc.reason}"
        )
        return (f"<UNENCODABLE:{code_point}>", exc.start + 1)

    raise exc


# 2. Custom Framed Codec Functions (Mounted directly onto str.encode / bytes.decode)
def encode_telemetry_xor(text: str, errors: str = "strict") -> Tuple[bytes, int]:
    utf8_payload = text.encode("utf-8", errors=errors)
    masked = bytes(b ^ XOR_MASK for b in utf8_payload)
    framed_packet = MAGIC_HEADER + masked
    return (framed_packet, len(text))


def decode_telemetry_xor(raw_input: Union[bytes, memoryview], errors: str = "strict") -> Tuple[str, int]:
    # CPython's codec layer may supply a memoryview; normalize to immutable bytes
    raw_bytes = bytes(raw_input)
    if not raw_bytes.startswith(MAGIC_HEADER):
        raise ValueError(f"Invalid framing signature: expected {MAGIC_HEADER!r}, got {raw_bytes[:2]!r}")

    unmasked = bytes(b ^ XOR_MASK for b in raw_bytes[len(MAGIC_HEADER) :])
    decoded_text = unmasked.decode("utf-8", errors=errors)
    return (decoded_text, len(raw_bytes))


def telemetry_codec_search_hook(normalized_name: str) -> Optional[codecs.CodecInfo]:
    """Search function registered in CPython's internal codec lookup table."""
    if normalized_name == CODEC_NAME:
        return codecs.CodecInfo(
            name=CODEC_NAME,
            encode=encode_telemetry_xor,
            decode=decode_telemetry_xor,
        )
    return None


# --- Execution Environment ---

# Register both our custom error handler and custom codec into CPython's C runtime
codecs.register_error("quarantine_hex", quarantine_corrupt_bytes_handler)
codecs.register(telemetry_codec_search_hook)

try:
    print("\n--- Diagnostic 1: Native str.encode() & bytes.decode() via Custom CodecInfo ---")
    # Lookup verifies CPython cached our CodecInfo struct inside its internal C registry
    codec_info = codecs.lookup("telemetry-xor-v1")  # CPython normalizes hyphens to underscores
    print(f"  → CPython Codec Registry Hit : {codec_info!r}")

    original_msg = "NODE=JORHAT_DC01::TEMP=38.4C::STATUS=OK"
    wire_frame: bytes = original_msg.encode("telemetry-xor-v1")
    recovered_msg: str = wire_frame.decode("telemetry-xor-v1")

    print(f"  → Native .encode() Wire Hex  : {wire_frame[:14].hex().upper()}... ({len(wire_frame)} bytes)")
    print(f"  → Native .decode() Roundtrip : {recovered_msg}")
    print(f"  → Exact Match Verified?      : {recovered_msg == original_msg}")

    print("\n--- Diagnostic 2: Mid-Stream Fault Quarantine on Corrupted Network Frames ---")
    # Simulate a raw UTF-8 wire packet struck by two stray non-UTF8 bit flips (0xFF and 0xFE)
    corrupted_packet = b"SENSOR_OK|" + b"\xff" + b"|TEMP=41C|" + b"\xfe" + b"|END_FRAME"

    # Standard 'strict' crashes; 'ignore' silently deletes evidence; 'quarantine_hex' recovers & audits!
    recovered_stream = corrupted_packet.decode("utf-8", errors="quarantine_hex")

    print(f"  → Raw Corrupted Packet       : {corrupted_packet!r}")
    print(f"  → Quarantined Decoded Output : {recovered_stream}")
    print(f"  → Forensic Faults Logged     : {len(CORRUPTION_AUDIT_LOG)}")
    for entry in CORRUPTION_AUDIT_LOG:
        print(f"      * {entry}")

    print("\n--- Diagnostic 3: Composing Custom Codec + Custom Error Handler Together ---")
    # Corrupt byte 5 inside an encoded XOR wire frame so unmasking yields an invalid UTF-8 byte (0xFF)
    tampered_frame = bytearray(wire_frame)
    tampered_frame[5] = 0xFF ^ XOR_MASK
    composed_recovery = bytes(tampered_frame).decode("telemetry-xor-v1", errors="quarantine_hex")
    print(f"  → Composed Codec Recovery    : {composed_recovery}")

finally:
    # Python 3.10+ supports cleanly unregistering custom codec search functions
    if hasattr(codecs, "unregister"):
        codecs.unregister(telemetry_codec_search_hook)

print(
    "\nStatus: Python fundamentals verified. Native encode/decode pipelines extended via codecs.register() and codecs.register_error()."
)