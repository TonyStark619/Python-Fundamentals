# Phase 3, Day 55: Python Fundamentals - Context Managers & Dunder Methods
import time

print("--- Booting Python Fundamental Resource Management ---")

# 1. The Context Manager Class Architecture
class SecureDatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connected = False

    # Executed automatically when the 'with' block opens
    def __enter__(self):
        print(f"\n[System] __enter__ triggered: Opening secure connection to '{self.db_name}'...")
        time.sleep(0.5)
        self.connected = True
        print(f"[System] Connection established. Resource locked.")
        return self  # The object returned here is bound to the 'as' variable

    # Executed automatically when the 'with' block closes, EVEN IF an error occurs
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"\n[System] __exit__ triggered: Safely terminating connection to '{self.db_name}'...")
        self.connected = False
        
        # If an exception was thrown inside the block, exc_type will catch it
        if exc_type:
            print(f"[Warning] Handled internal exception: {exc_val}")
        
        print("[System] Resource unlocked. Memory leak prevented.")
        # Returning True suppresses the exception. Returning False lets it bubble up.
        return True 

    def execute_query(self, query):
        if not self.connected:
            raise RuntimeError("Database is disconnected.")
        print(f"  -> [DB Node] Executing: '{query}'")
        
        if "DROP" in query:
            raise ValueError("Unauthorized Destructive Action Detected!")
            
        return "200 OK: Query successful."

# --- Execution Environment ---

# Scenario 1: Successful Execution
print("\n--- Scenario 1: Standard Execution ---")
with SecureDatabaseConnection("Production_DB") as db:
    db.execute_query("SELECT * FROM users")

# Scenario 2: Fatal Error Execution (Testing the safety net)
print("\n--- Scenario 2: Fatal Error Injection ---")
with SecureDatabaseConnection("Production_DB") as db:
    db.execute_query("SELECT * FROM payments")
    # This will trigger an internal exception, but __exit__ guarantees safe closure
    db.execute_query("DROP TABLE users")

print("\nStatus: Python fundamentals verified. Dunder methods successfully managed resource lifecycle and intercepted runtime exceptions.")