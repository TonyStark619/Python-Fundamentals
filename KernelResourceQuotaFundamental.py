# Phase 3, Day 212: Python Fundamentals - POSIX Kernel Resource Quotas (resource)
import sys
import os

# Verify POSIX compliance (Required for OS-level resource limits)
if os.name != 'posix':
    print("[ALERT] Resource limits require a POSIX OS (Linux/Unix/Mac). Windows is not supported.")
    sys.exit(0)

import resource
import time

print("--- Booting OS-Level Kernel Resource Quota Manager ---")

# 1. Define the mathematical memory limit (e.g., 50 Megabytes)
LIMIT_IN_MEGABYTES = 50
LIMIT_IN_BYTES = LIMIT_IN_MEGABYTES * 1024 * 1024

def lock_memory_boundaries():
    """
    Communicates directly with the Linux Kernel to enforce physical memory bounds.
    """
    print(f"  [Kernel] Requesting strict {LIMIT_IN_MEGABYTES} MB RAM quota from the OS...")
    
    # RLIMIT_AS = Address Space (The maximum area of memory the process can map)
    # The tuple is (Soft Limit, Hard Limit)
    resource.setrlimit(resource.RLIMIT_AS, (LIMIT_IN_BYTES, LIMIT_IN_BYTES))
    
    print("  [Kernel] Quota locked. If breached, the OS will mathematically sever allocations.")

def simulate_rogue_memory_leak():
    """
    A deliberately disastrous function that attempts to consume infinite RAM.
    """
    print("\n  [Subprocess] Initiating heavy data aggregation (Simulating Memory Leak)...")
    
    massive_payload = []
    megabytes_allocated = 0
    
    try:
        while True:
            # We attempt to allocate 1 Megabyte of raw characters at a time
            massive_payload.append("X" * (1024 * 1024))
            megabytes_allocated += 1
            print(f"    -> Aggregated: {megabytes_allocated} MB")
            
            # Artificial delay so you can watch it climb
            time.sleep(0.05)
            
    except MemoryError:
        # THE MAGIC: Python throws a MemoryError NOT because the physical server ran out of RAM,
        # but because the Linux Kernel violently rejected the allocation request.
        print(f"\n[ALERT] OS KERNEL INTERVENTION TRIGGERED!")
        print(f"  -> Allocation denied at {megabytes_allocated} MB.")
        print(f"  -> Physical server RAM protected from process exhaustion.")

# --- Execution Environment ---

# 2. Lock the hardware limits before executing risky logic
lock_memory_boundaries()

# 3. Unleash the rogue function
simulate_rogue_memory_leak()

print("\nStatus: Python fundamentals verified. Rogue memory leaks successfully contained via POSIX RLIMIT constraints.")