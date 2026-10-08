# Phase 3, Day 195: Python Fundamentals - Live Thread Forensics (sys._current_frames)
import sys
import threading
import traceback
import time

print("--- Booting CPython Deadlock Forensics Engine ---")

# 1. Simulate the Enterprise Deadlock
lock_A = threading.Lock()
lock_B = threading.Lock()

def faulty_transaction_alpha():
    """Simulates a thread that grabs Lock A, then waits for Lock B."""
    lock_A.acquire()
    time.sleep(0.1) # Simulating network delay
    print("  [Thread Alpha] Waiting for Lock B...")
    lock_B.acquire() # CRITICAL DEADLOCK: Freezes here permanently

def faulty_transaction_beta():
    """Simulates a thread that grabs Lock B, then waits for Lock A."""
    lock_B.acquire()
    time.sleep(0.1) # Simulating network delay
    print("  [Thread Beta] Waiting for Lock A...")
    lock_A.acquire() # CRITICAL DEADLOCK: Freezes here permanently

# --- Execution Environment ---

# Spawn the threads and trigger the absolute gridlock
thread_1 = threading.Thread(target=faulty_transaction_alpha, name="WorkerThread-Alpha")
thread_2 = threading.Thread(target=faulty_transaction_beta, name="WorkerThread-Beta")

thread_1.start()
thread_2.start()

time.sleep(0.5) # Give the gridlock half a second to completely freeze the application

print("\n--- [ALERT] SYSTEM GRIDLOCK DETECTED ---")
print("  [System] Executing God-Mode C-Level Thread Sweep...\n")

# THE MAGIC: sys._current_frames() pulls the raw C-memory pointers of every active thread
frozen_threads = sys._current_frames()

for thread_id, frame in frozen_threads.items():
    # We map the raw thread ID to the human-readable thread name if it exists in the threading module
    thread_name = "MainThread"
    for t in threading.enumerate():
        if t.ident == thread_id:
            thread_name = t.name
            
    print(f"==================================================")
    print(f"THREAD ISOLATED: {thread_name} (ID: {thread_id})")
    
    # We extract the exact live stack trace from the frozen memory frame
    stack_trace = traceback.extract_stack(frame)
    
    # Isolate the very last action the thread took before freezing
    last_action = stack_trace[-1]
    
    print(f"  -> Frozen in File: {last_action.filename}")
    print(f"  -> Frozen in Function: '{last_action.name}()'")
    print(f"  -> Exact Line of Code: Line {last_action.lineno}")
    print(f"  -> Executing Statement: {last_action.line}")
    print(f"==================================================\n")

print("Status: Python fundamentals verified. Deadlocked C-level threads successfully mapped and isolated via live frame extraction.")

# Note: We must forcefully exit because the background threads are permanently deadlocked
import os
os._exit(0)