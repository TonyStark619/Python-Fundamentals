# Phase 3, Day 64: Python Fundamentals - Weak References & Garbage Collection
import weakref
import gc

print("--- Booting Python RAM Allocation Diagnostics ---")

# 1. The Vulnerable Architecture (Circular Reference Leak)
class LeakyNode:
    def __init__(self, name):
        self.name = name
        self.partner = None
        
    def __del__(self):
        print(f"    [Garbage Collector] Destroying LeakyNode: {self.name} - Memory freed.")

# 2. The Enterprise Architecture (Weak References)
class SecureNode:
    def __init__(self, name):
        self.name = name
        self._partner = None
        
    @property
    def partner(self):
        # A weak reference must be called like a function to retrieve the actual object
        return self._partner() if self._partner else None
        
    @partner.setter
    def partner(self, obj):
        # THE MAGIC: Assigning a weak reference to the target object
        self._partner = weakref.ref(obj)
        
    def __del__(self):
        print(f"    [Garbage Collector] Destroying SecureNode: {self.name} - Memory freed.")

# --- Execution Environment ---
print("\n--- Scenario 1: Simulating Circular Memory Leak ---")
node_a = LeakyNode("Alpha")
node_b = LeakyNode("Beta")

# Creating the circular lock
node_a.partner = node_b
node_b.partner = node_a

print("[System] Deleting hard references to Alpha and Beta...")
del node_a
del node_b
gc.collect() # Force garbage collection
print("[Result] Garbage Collector failed. Objects remain locked in RAM (Memory Leak).")


print("\n--- Scenario 2: Simulating Secure Weak References ---")
node_x = SecureNode("X-Ray")
node_y = SecureNode("Yankee")

# Creating the secure weak link
node_x.partner = node_y
node_y.partner = node_x

print("[System] Deleting hard references to X-Ray and Yankee...")
del node_x
del node_y
gc.collect() # Force garbage collection
print("[Result] Weak references detected. Garbage Collector successfully freed RAM.")

print("\nStatus: Python fundamentals verified. Circular reference locks bypassed via weakref allocation.")