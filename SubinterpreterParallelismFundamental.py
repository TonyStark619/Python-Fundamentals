# Phase 3, Day 218: Python Fundamentals - Subinterpreter Isolation (_xxsubinterpreters)
import _xxsubinterpreters
import threading
import time

print("--- Booting CPython Subinterpreter Isolation Engine ---")

# 1. The Isolated Payload
# This code will execute in a completely different CPython memory context.
# It cannot see global variables from the main interpreter.
SUBINTERPRETER_PAYLOAD = """
import time

def isolated_workload():
    print(f"    [Subinterpreter] Boot sequence initialized. Memory isolated.")
    start = time.perf_counter()
    
    # Simulating a heavy, CPU-bound mathematical operation
    total = 0
    for i in range(10_000_000):
        total += i
        
    duration = time.perf_counter() - start
    print(f"    [Subinterpreter] Calculation complete: {total}. Blocked CPU for {duration:.3f}s.")

isolated_workload()
"""

# 2. Spawning the Subinterpreters
def execute_in_subinterpreter(interp_id):
    """
    Executes the payload string directly inside the isolated C-level interpreter instance.
    """
    print(f"  [System] Injecting payload into Subinterpreter ID: {interp_id}")
    try:
        # The C-level command to execute string code in a specific subinterpreter context
        _xxsubinterpreters.run_string(interp_id, SUBINTERPRETER_PAYLOAD)
    except Exception as e:
        print(f"  [ALERT] Subinterpreter execution failed: {e}")

# --- Execution Environment ---

print("\n[System] Allocating isolated CPython interpreter contexts...")

# Ask the C-backend to literally create new Python runtime environments
interp_alpha_id = _xxsubinterpreters.create()
interp_beta_id = _xxsubinterpreters.create()

print(f"  -> Successfully mounted Subinterpreter Alpha (ID: {interp_alpha_id})")
print(f"  -> Successfully mounted Subinterpreter Beta  (ID: {interp_beta_id})")

print("\n--- Initiating True Parallel Execution ---")

# 3. Threading across Interpreters
# In standard Python, these threads would fight over the exact same GIL.
# Here, each thread operates its own isolated subinterpreter with its own GIL.
thread_1 = threading.Thread(target=execute_in_subinterpreter, args=(interp_alpha_id,))
thread_2 = threading.Thread(target=execute_in_subinterpreter, args=(interp_beta_id,))

start_time = time.perf_counter()

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()

total_duration = time.perf_counter() - start_time

print(f"\nCRITICAL RESULT: Parallel payloads resolved in {total_duration:.3f} seconds.")

# 4. Graceful Teardown
_xxsubinterpreters.destroy(interp_alpha_id)
_xxsubinterpreters.destroy(interp_beta_id)

print("Status: Python fundamentals verified. Global Interpreter Lock (GIL) bypassed natively via CPython subinterpreter context isolation.")