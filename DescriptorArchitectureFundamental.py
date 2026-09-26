# Phase 3, Day 178: Python Fundamentals - Data Descriptors (__get__ & __set__)

print("--- Booting Python Enterprise Descriptor Protocol ---")

# 1. The Descriptor (The Validation Engine)
class StrictlyTypedInteger:
    """
    A descriptor that intercepts all assignments to an attribute.
    It mathematically guarantees type safety and boundary enforcement.
    """
    def __init__(self, min_val: int, max_val: int):
        self.min_val = min_val
        self.max_val = max_val
        self.name = None # Will be set dynamically by __set_name__ (Python 3.6+)

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        # Intercept the request and pull from the private dictionary
        return getattr(instance, self.name, None)

    def __set__(self, instance, value):
        print(f"  [Descriptor Intercept] Validating '{self.name[1:]}' assignment: {value}")
        
        if not isinstance(value, int):
            raise TypeError(f"CRITICAL: {self.name[1:]} must be a strict integer, got {type(value).__name__}.")
            
        if value < self.min_val or value > self.max_val:
            raise ValueError(f"CRITICAL: {self.name[1:]} out of bounds. Must be between {self.min_val} and {self.max_val}.")
            
        # Write the validated data securely into the object's memory
        setattr(instance, self.name, value)
        print("  -> Validation passed. Memory state committed.")

# 2. The Enterprise Data Model
class CorporateServerNode:
    """
    The main class simply assigns the descriptors. Zero @property boilerplate.
    """
    # These descriptors live at the class level but govern instance-level data
    cpu_cores = StrictlyTypedInteger(min_val=4, max_val=128)
    ram_gb = StrictlyTypedInteger(min_val=16, max_val=2048)
    
    def __init__(self, name, cores, ram):
        self.name = name
        # When we assign these, the Descriptor's __set__ method is automatically triggered
        self.cpu_cores = cores
        self.ram_gb = ram

# --- Execution Environment ---
print("\n[System] Spawning Validated Corporate Server Nodes...")

print("\n--- Scenario 1: Compliant Instantiation ---")
node_alpha = CorporateServerNode("Alpha_01", cores=32, ram=256)
print(f"[Success] Node configured with {node_alpha.cpu_cores} cores.")

print("\n--- Scenario 2: Boundary Violation Intercept ---")
try:
    node_beta = CorporateServerNode("Beta_02", cores=2, ram=64)
except Exception as e:
    print(e)

print("\n--- Scenario 3: Type Safety Violation Intercept ---")
try:
    node_gamma = CorporateServerNode("Gamma_03", cores=16, ram="512GB")
except Exception as e:
    print(e)

print("\nStatus: Python fundamentals verified. Descriptor protocol successfully hijacked memory assignment for silent C-level validation.")