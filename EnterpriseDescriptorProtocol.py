# Phase 3, Day 213: Python Fundamentals - The Descriptor Protocol (__get__, __set__)
import sys

print("--- Booting Enterprise Descriptor Validation Engine ---")

# 1. The Descriptor Architectures (Reusable Data C-Level Validators)
class StrictTypeDescriptor:
    """
    A low-level descriptor that intercepts attribute assignment 
    to physically enforce strict memory typing.
    """
    def __init__(self, expected_type):
        self.expected_type = expected_type

    # Triggered automatically when the class is first loaded into RAM
    def __set_name__(self, owner, name):
        # We dynamically save the variable name so we know what we are managing (e.g., 'age' or 'salary')
        self.public_name = name
        self.private_name = '_' + name

    # Intercepts the '.' access operator (e.g., obj.age)
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        print(f"    [Descriptor Hook] Read access authorized for '{self.public_name}'.")
        return getattr(obj, self.private_name)

    # Intercepts the '=' assignment operator (e.g., obj.age = 25)
    def __set__(self, obj, value):
        print(f"    [Descriptor Hook] Intercepted assignment to '{self.public_name}'. Initiating type verification...")
        
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"ZERO-TRUST VIOLATION: '{self.public_name}' requires strict {self.expected_type.__name__} memory. "
                f"Payload received type: {type(value).__name__}."
            )
            
        print(f"    [Descriptor Hook] Type verified. Writing value to instance dictionary.")
        setattr(obj, self.private_name, value)


# 2. The Enterprise Class
class UserPayload:
    """
    Notice there is absolutely no __init__ logic required for type checking, 
    and ZERO @property decorators. The architecture enforces itself natively.
    """
    username = StrictTypeDescriptor(str)
    auth_level = StrictTypeDescriptor(int)

    def __init__(self, username, auth_level):
        # These assignments trigger the __set__ method of the descriptors automatically
        self.username = username
        self.auth_level = auth_level


# --- Execution Environment ---

print("\n--- Diagnostic 1: Valid Enterprise Payload ---")
try:
    valid_user = UserPayload("Admin_Alpha", 9)
    print(f"Success: Isolated User -> {valid_user.username} | Level {valid_user.auth_level}")
except TypeError as e:
    print(e)

print("\n--- Diagnostic 2: Lethal Type Injection Attack ---")
try:
    # A hacker or careless microservice tries to pass a string instead of an integer for auth_level
    corrupt_user = UserPayload("Hacker_Beta", "NINE")
except TypeError as e:
    print(f"\n[ALERT] INTERCEPTED FAULT: {e}")

print("\nStatus: Python fundamentals verified. Standard decorators bypassed via reusable C-level Descriptor Protocol assignments.")