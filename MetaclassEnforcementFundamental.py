# Phase 3, Day 180: Python Fundamentals - Metaclasses & Compile-Time Dictatorship
import re

print("--- Booting Python Enterprise Metaclass Compiler ---")

# 1. The Metaclass (The Architect)
class StrictNamingMeta(type):
    """
    This Metaclass intercepts the creation of any class that inherits from it.
    It mathematically scans the raw namespace dictionary before allocation in RAM.
    """
    def __new__(mcs, name, bases, namespace):
        print(f"  [Metaclass Intercept] Scanning blueprint for class: '{name}'...")
        
        # Define a regex for snake_case (lowercase letters, numbers, and underscores only)
        snake_case_pattern = re.compile(r'^[a-z_][a-z0-9_]*$')
        
        for attr_name, attr_value in namespace.items():
            # We ignore Python's internal dunder methods (like __init__)
            if attr_name.startswith("__") and attr_name.endswith("__"):
                continue
                
            # If a method or variable is NOT snake_case, mathematically reject the class
            if not callable(attr_value):
                continue # Skip standard variables for this test, focusing on functions
                
            if not snake_case_pattern.match(attr_name):
                raise SyntaxError(
                    f"\nCRITICAL ARCHITECTURE VIOLATION in '{name}':\n"
                    f"  -> Method '{attr_name}' violates enterprise snake_case standards.\n"
                    f"  -> Class creation aborted by Metaclass."
                )
                
        print(f"  [Metaclass Approval] Class '{name}' complies with enterprise architecture. Allocating to RAM.")
        # If everything passes, we use the super() Metaclass to physically build the class
        return super().__new__(mcs, name, bases, namespace)

# --- Execution Environment ---

print("\n--- Scenario 1: Compiling a Compliant Subclass ---")
try:
    # By specifying metaclass=StrictNamingMeta, we surrender control to the Architect
    class CompliantService(metaclass=StrictNamingMeta):
        def initialize_database(self):
            return "DB Connected"
            
        def execute_payload(self):
            return "Payload Sent"
            
    print("Result: Success. Developers can use CompliantService normally.")
except Exception as e:
    print(e)


print("\n--- Scenario 2: Compiling a Non-Compliant Subclass ---")
try:
    # A junior developer tries to use camelCase in an enterprise Python environment
    class NonCompliantService(metaclass=StrictNamingMeta):
        def initializeDatabase(self): # VIOLATION
            return "DB Connected"
            
except Exception as e:
    # The compiler catches it instantly. The class never even makes it into memory.
    print(f"{type(e).__name__}: {e}")

print("\nStatus: Python fundamentals verified. Metaclass protocol successfully hijacked class allocation and enforced architectural compliance.")