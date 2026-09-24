# Phase 3, Day 175: Python Fundamentals - Context Managers & Atomic Transactions
import copy

print("--- Booting Python Atomic Database Engine ---")

class AtomicTransaction:
    """
    An enterprise context manager that intercepts execution block states.
    It guarantees ACID compliance: if any code fails, all memory is instantly rolled back.
    """
    def __init__(self, target_database):
        self.target_database = target_database
        self.backup_snapshot = None

    def __enter__(self):
        print("  [System] Entering Atomic Zone. Creating deep memory snapshot...")
        # Deepcopy guarantees nested structures are fully backed up in a separate RAM block
        self.backup_snapshot = copy.deepcopy(self.target_database)
        return self.target_database

    def __exit__(self, exc_type, exc_value, traceback):
        # If exc_type is not None, an error occurred inside the 'with' block
        if exc_type is not None:
            print(f"\n  [CRITICAL INTERCEPT] Exception detected: {exc_type.__name__} - {exc_value}")
            print("  [System] Rolling back memory to previous safe snapshot to prevent corruption.")
            
            # Wipe the corrupted data and restore from the backup
            self.target_database.clear()
            self.target_database.update(self.backup_snapshot)
            
            # Return True to mathematically suppress the exception from crashing the whole server
            return True 
        
        print("\n  [System] Execution successful. State permanently committed.")
        return False

# --- Execution Environment ---
# Simulating a live in-memory database
live_database = {"User_1": "Alpha", "User_2": "Beta", "System_Balance": 1000}

print("\n--- Scenario 1: Successful Transaction ---")
with AtomicTransaction(live_database) as db:
    print("  -> Executing updates...")
    db["User_3"] = "Gamma"
    db["System_Balance"] -= 200

print(f"Final State: {live_database}")


print("\n--- Scenario 2: Corrupted Transaction ---")
with AtomicTransaction(live_database) as db:
    print("  -> Executing updates...")
    db["User_4"] = "Delta" # This succeeds
    db["System_Balance"] -= 500 # This succeeds
    
    print("  -> Triggering fatal mathematical error...")
    # This divides by zero and instantly crashes the block
    crash_variable = 10 / 0 
    
    db["User_5"] = "Echo" # This line is never reached

# The data was rolled back, so User_4 should NOT exist, and Balance should NOT be deducted
print(f"Final State: {live_database}")

print("\nStatus: Python fundamentals verified. Context managers successfully enforced atomic memory safety.")