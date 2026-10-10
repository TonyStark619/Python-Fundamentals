# Phase 3, Day 197: Python Fundamentals - OS-Level Signal Interception (signal)
import signal
import sys
import time

print("--- Booting Enterprise OS Signal Interceptor ---")

# 1. The Global Server State (Vulnerable to sudden death)
active_transactions = [1044, 1045, 1046]
is_shutting_down = False

# 2. The Emergency Protocol (The Hook)
def graceful_shutdown_protocol(signum, frame):
    """
    This function intercepts the OS kill switch.
    signum: The numerical ID of the signal (e.g., 2 for SIGINT)
    frame: The live execution frame at the exact millisecond the signal hit
    """
    global is_shutting_down
    
    print("\n\n  [ALERT] OS-LEVEL KILL SIGNAL INTERCEPTED.")
    print(f"  [System] Signal {signum} caught. Freezing main thread...")
    
    is_shutting_down = True
    
    print("  [Emergency Protocol] Dumping volatile RAM states to SSD...")
    # Simulate writing the critical data to a safe location before dying
    time.sleep(1.5)
    print(f"  [Emergency Protocol] State saved successfully. Unresolved transactions: {active_transactions}")
    
    print("  [System] Graceful exit authorized. Terminating process.")
    sys.exit(0) # Properly kill the server now that data is safe

# --- Execution Environment ---

# 3. Arming the Interceptor
# We tell the OS: "If the user hits Ctrl+C (SIGINT), DO NOT kill the program. Call my protocol instead."
signal.signal(signal.SIGINT, graceful_shutdown_protocol)
# SIGTERM is the standard kill signal sent by Docker, Kubernetes, and Linux 'kill' commands
signal.signal(signal.SIGTERM, graceful_shutdown_protocol)

print("\n[System] Signal hooks armed. Server entering infinite loop.")
print("INSTRUCTION: Press 'Ctrl+C' in your terminal right now to trigger the kill switch.\n")

try:
    # 4. The Main Application Loop (Simulating a running server)
    counter = 0
    while not is_shutting_down:
        print(f"  -> Processing server frame {counter}... (Waiting for Ctrl+C)")
        time.sleep(1)
        counter += 1
        
except Exception as e:
    # A standard try/except WILL NOT catch a SIGINT properly without the signal hook
    print(f"Exception: {e}")

print("Status: Python fundamentals verified. OS interrupts successfully hijacked for enterprise fault tolerance.")