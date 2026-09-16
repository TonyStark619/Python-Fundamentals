# Phase 3, Day 60: Python Fundamentals - Multiprocessing & GIL Bypass
import time
import threading
import multiprocessing

print("--- Booting Python Multicore Optimization Diagnostics ---")

def cpu_heavy_computation(task_id, iterations):
    """A mathematically intensive task to simulate data processing or model training."""
    print(f"  [Task {task_id}] Initiating compute loop ({iterations} iterations)...")
    total = 0
    for i in range(iterations):
        total += i * i
    return total

# 1. The Threading Bottleneck (Restricted by the GIL)
def execute_threading():
    print("\n[System] Spawning 2 Threads (Sharing 1 GIL)...")
    start_time = time.time()
    
    t1 = threading.Thread(target=cpu_heavy_computation, args=("Thread-1", 15_000_000))
    t2 = threading.Thread(target=cpu_heavy_computation, args=("Thread-2", 15_000_000))
    
    t1.start(); t2.start()
    t1.join(); t2.join()
    
    duration = time.time() - start_time
    print(f"[Result] Threading Execution Time: {duration:.2f} seconds")
    return duration

# 2. The Multiprocessing Architecture (Bypassing the GIL)
def execute_multiprocessing():
    print("\n[System] Spawning 2 Independent Processes (Parallel Cores)...")
    start_time = time.time()
    
    p1 = multiprocessing.Process(target=cpu_heavy_computation, args=("Process-1", 15_000_000))
    p2 = multiprocessing.Process(target=cpu_heavy_computation, args=("Process-2", 15_000_000))
    
    p1.start(); p2.start()
    p1.join(); p2.join()
    
    duration = time.time() - start_time
    print(f"[Result] Multiprocessing Execution Time: {duration:.2f} seconds")
    return duration

# --- Execution Environment ---
if __name__ == '__main__':
    # Due to OS process spawning rules (especially on Windows), 
    # multiprocessing code MUST be guarded by __main__.
    
    thread_time = execute_threading()
    process_time = execute_multiprocessing()
    
    efficiency_gain = ((thread_time - process_time) / thread_time) * 100
    
    print(f"\n--- Diagnostic Conclusion ---")
    print(f"Parallel Core Efficiency Gain: {efficiency_gain:.1f}% faster.")
    print("Status: Python fundamentals verified. Global Interpreter Lock successfully bypassed.")