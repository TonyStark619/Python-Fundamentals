# Phase 3, Day 214: Python Fundamentals - C-Level RAM Allocation Profiling (tracemalloc)
import tracemalloc
import time

print("--- Booting CPython Hardware Allocation Profiler ---")

def rogue_enterprise_transaction():
    """
    Simulates a deeply buried function that recklessly allocates massive RAM blocks.
    """
    print("  [Subprocess] Executing complex data aggregation...")
    # This list comprehension will silently request megabytes of physical RAM from the OS
    heavy_data_buffer = [str(x) * 100 for x in range(500_000)]
    return heavy_data_buffer

# --- Execution Environment ---

# 1. Arm the C-Level Allocator Hook
print("  [System] Injecting tracking hooks into C-level malloc()...")
# Tracing up to 5 stack frames deep to pinpoint the exact caller
tracemalloc.start(5) 

# 2. Capture the exact state of physical RAM before the transaction
snapshot_alpha = tracemalloc.take_snapshot()
print("  [System] Memory Snapshot Alpha captured.")

# 3. Execute the vulnerable logic
rogue_payload = rogue_enterprise_transaction()

# 4. Capture the exact state of physical RAM after the transaction
snapshot_beta = tracemalloc.take_snapshot()
print("  [System] Memory Snapshot Beta captured.")

print("\n--- Initiating Cross-Snapshot Delta Analysis ---")
# THE MAGIC: We ask CPython to subtract Snapshot Alpha from Snapshot Beta, 
# filtering strictly by the exact line of code ('lineno') that allocated the delta.
memory_delta = snapshot_beta.compare_to(snapshot_alpha, 'lineno')

print("\n[CRITICAL ALERTS] Top 3 RAM Allocation Sources Isolated:")

for index, stat in enumerate(memory_delta[:3], 1):
    # Extract the physical filepath, line number, and megabytes allocated
    frame = stat.traceback[0]
    allocated_mb = stat.size_diff / (1024 * 1024)
    
    print(f"\n  Violation #{index}:")
    print(f"    -> File: {frame.filename}")
    print(f"    -> Line of Code: {frame.lineno}")
    print(f"    -> Physical RAM Bleed: {allocated_mb:.2f} MB")
    
    # We even print the exact raw code that caused the leak
    with open(frame.filename, 'r') as f:
        lines = f.readlines()
        print(f"    -> Execution Statement: {lines[frame.lineno - 1].strip()}")

# Disarm the hook to restore normal CPU performance
tracemalloc.stop()

print("\nStatus: Python fundamentals verified. Rogue physical RAM allocations mathematically mapped to exact source code lines via tracemalloc C-hooks.")