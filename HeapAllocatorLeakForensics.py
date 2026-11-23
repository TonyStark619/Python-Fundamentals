# Phase 3, Master Day 239: Python Fundamentals - PEP 454 C-Allocator Heap Forensics (tracemalloc)
import gc
import linecache
import tracemalloc
from typing import List

print("--- Booting CPython PEP 454 C-Allocator Heap Forensics Engine ---")

# Simulated global cache that silently leaks 4 KB telemetry frames without eviction
_UNBOUNDED_TELEMETRY_CACHE: List[bytearray] = []


def process_ephemeral_batch(iterations: int) -> int:
    """Healthy workload: allocates temporary buffers that are reclaimed immediately on exit."""
    checksum = 0
    for i in range(iterations):
        temp_frame = bytearray(2048)
        temp_frame[0] = i % 256
        checksum += temp_frame[0]
    return checksum


def ingest_leaky_telemetry_stream(packet_count: int) -> None:
    """Faulty workload: appends 4 KB payloads into a global list with zero eviction."""
    for seq in range(packet_count):
        # INTENTIONAL LEAK SITE: Every call retains a 4,096-byte C heap block permanently
        payload = bytearray(4096)
        payload[0] = seq % 256
        _UNBOUNDED_TELEMETRY_CACHE.append(payload)


def format_source_line(filename: str, lineno: int) -> str:
    line = linecache.getline(filename, lineno).strip()
    return line if line else "<unavailable>"


# --- Execution Environment ---

# 1. Hook CPython's C-level memory allocators (PyMem_Malloc / PyObject_Malloc) with 5-frame stack depth
tracemalloc.start(5)
print(f"  [C-Allocator Hook] tracemalloc armed with traceback depth = {tracemalloc.get_traceback_limit()} frames.")

try:
    # Establish clean baseline heap snapshot
    gc.collect()
    baseline_snapshot = tracemalloc.take_snapshot()

    print("\n--- Diagnostic 1: Running Mixed Healthy + Leaky Workloads ---")
    _ = process_ephemeral_batch(500)
    ingest_leaky_telemetry_stream(250)  # Leaks ~1.0 MB across 250 retained 4 KB blocks

    # Reclaim all unreachable ephemeral objects before taking the post-workload snapshot
    gc.collect()
    post_snapshot = tracemalloc.take_snapshot()

    # Strip out tracemalloc internals and frozen importlib frames to isolate application code
    noise_filters = (
        tracemalloc.Filter(False, tracemalloc.__file__),
        tracemalloc.Filter(False, "<frozen *>"),
        tracemalloc.Filter(False, "<unknown>"),
    )
    clean_baseline = baseline_snapshot.filter_traces(noise_filters)
    clean_post = post_snapshot.filter_traces(noise_filters)

    # Compute exact line-by-line C heap allocation deltas
    top_diffs = clean_post.compare_to(clean_baseline, "lineno")

    print("\n--- Diagnostic 2: Top Heap Growth Sites (Snapshot Diff by lineno) ---")
    for rank, stat in enumerate(top_diffs[:3], start=1):
        frame = stat.traceback[0]
        source_code = format_source_line(frame.filename, frame.lineno)
        print(
            f"  #{rank} Line {frame.lineno:3d} | Net Growth: {stat.size_diff:+10,d} bytes "
            f"({stat.count_diff:+4d} blocks) | Code: {source_code}"
        )

    print("\n--- Diagnostic 3: Reverse-Tracing a Live Object's Allocation Provenance ---")
    suspect_buffer = _UNBOUNDED_TELEMETRY_CACHE[-1]
    provenance_tb = tracemalloc.get_object_traceback(suspect_buffer)

    print(f"  → Suspect Object Address : {hex(id(suspect_buffer))} ({len(suspect_buffer):,} bytes)")
    if provenance_tb is not None:
        print("  → Exact C-Allocator Call Stack (Innermost -> Outermost):")
        for frame in provenance_tb:
            print(f"      * Line {frame.lineno:3d}: {format_source_line(frame.filename, frame.lineno)}")

    current_bytes, peak_bytes = tracemalloc.get_traced_memory()
    print("\n--- Diagnostic 4: Exact C-Heap Watermark Telemetry ---")
    print(f"  → Live Retained Heap : {current_bytes / 1024:,.2f} KiB")
    print(f"  → Peak High-Water    : {peak_bytes / 1024:,.2f} KiB")

finally:
    _UNBOUNDED_TELEMETRY_CACHE.clear()
    tracemalloc.stop()

print(
    "\nStatus: Python fundamentals verified. Silent heap leaks isolated to exact source lines via PEP 454 tracemalloc C-allocator hooks."
)