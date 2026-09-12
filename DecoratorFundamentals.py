# Phase 3, Day 47: Python Fundamentals - Decorators & Higher-Order Functions
import time
import random
from functools import wraps

print("--- Booting Python Fundamental Decorator Diagnostics ---")

# 1. The Decorator Engine
# A decorator is a function that takes another function as an argument.
def enterprise_retry(max_attempts=3, delay_seconds=1):
    def decorator(func):
        # @wraps preserves the original function's name and metadata
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    print(f"[Wrapper] Attempting execution {attempts + 1}/{max_attempts}...")
                    # Execute the actual function
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    print(f"[Wrapper] Execution failed: {e}")
                    if attempts >= max_attempts:
                        print("[Wrapper] Max retries exhausted. Escalating failure.")
                        raise
                    print(f"[Wrapper] Retrying in {delay_seconds} seconds...\n")
                    time.sleep(delay_seconds)
        return wrapper
    return decorator

# 2. Applying the Decorator
# We mathematically inject the retry logic into this fragile function simply by tagging it.
@enterprise_retry(max_attempts=4, delay_seconds=0.5)
def unstable_database_call(query):
    print(f"[DB Node] Executing query: '{query}'")
    
    # Simulating a random network failure (80% chance to fail)
    if random.random() < 0.8:
        raise ConnectionError("Network packet dropped.")
        
    return "SUCCESS: 200 OK. Data retrieved."

# --- Execution Environment ---
print("\n[System] Initiating fragile network operations...")

try:
    result = unstable_database_call("SELECT * FROM users")
    print(f"\n--- Final Payload ---\n{result}")
except ConnectionError:
    print("\n--- Final Payload ---\nCRITICAL FAILURE: Unable to establish connection.")

print("\nStatus: Python fundamentals verified. Higher-order function wrapping successfully intercepted and handled exceptions.")