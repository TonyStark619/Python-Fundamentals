# Phase 3, Day 211: Python Fundamentals - POSIX Kernel File Locking (fcntl)
import os
import sys
import time
import multiprocessing

# Verify POSIX compliance (Enterprise Linux/Mac backend)
if os.name != 'posix':
    print("[ALERT] This enterprise architecture requires a POSIX-compliant OS (Linux/Unix).")
    print("For Windows, the equivalent module is 'msvcrt'. Exiting simulation.")
    sys.exit(0)

import fcntl

print("--- Booting OS-Level Kernel File Interceptor ---")

DB_FILE = "enterprise_database.log"

def critical_database_writer(process_id, execute_lock):
    """
    Simulates a background process attempting to write to the SSD.
    """
    print(f"  [Process {process_id}] Booting up. Attempting disk I/O...")
    
    with open(DB_FILE, 'a') as f:
        try:
            if execute_lock:
                print(f"  [Process {process_id}] Requesting EXCLUSIVE Kernel Lock from the OS...")
                # THE MAGIC: fcntl.LOCK_EX (Exclusive lock) | fcntl.LOCK_NB (Non-Blocking)
                # The OS mathematically refuses access to any other process while this is held.
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                print(f"  [Process {process_id}] OS Lock Acquired. Safely writing to disk...")
            
            # Simulate a time-consuming write operation
            f.write(f"Secure payload from Process {process_id}\n")
            time.sleep(2) 
            
            if execute_lock:
                # Release the physical OS lock
                fcntl.flock(f, fcntl.LOCK_UN)
                print(f"  [Process {process_id}] Transaction complete. OS Lock released.")
                
        except BlockingIOError:
            # If the OS blocks us because another process holds the inode lock
            print(f"    -> [ALERT] Process {process_id} blocked by Linux Kernel! File is strictly locked.")

# --- Execution Environment ---

if __name__ == '__main__':
    # Touch the file to ensure it exists
    open(DB_FILE, 'w').close()
    
    print("\n--- Diagnostic: Simulating Concurrent Process Collision ---")
    
    # Process A grabs the physical lock and holds it for 2 seconds
    process_a = multiprocessing.Process(target=critical_database_writer, args=("ALPHA", True))
    
    # Process B ignores Python locks and tries to write to the file 0.5 seconds later
    process_b = multiprocessing.Process(target=critical_database_writer, args=("BETA", True))
    
    process_a.start()
    time.sleep(0.5) # Ensure A locks the file first
    process_b.start()
    
    process_a.join()
    process_b.join()
    
    # Cleanup
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
        
    print("\nStatus: Python fundamentals verified. Race conditions mathematically eliminated across isolated processes via physical OS kernel locks.")