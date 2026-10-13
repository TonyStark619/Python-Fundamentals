# Phase 3, Day 201: Python Fundamentals - GC Memory Forensics (gc.get_referrers)
import gc
import sys

print("--- Booting CPython Garbage Collection Forensics Engine ---")

class LeakedEnterprisePayload:
    """A massive memory object that we are going to intentionally lose track of."""
    def __init__(self, identifier):
        self.identifier = identifier
        self.heavy_data = [x for x in range(1000)] # Simulating RAM weight
        
    def __repr__(self):
        return f"<LeakedPayload: {self.identifier}>"

# 1. Simulate the Memory Leak
# A rogue global dictionary forgotten by the developer, hiding deep in the system
_hidden_rogue_cache = {}

def execute_vulnerable_transaction():
    """Simulates a function that creates data but accidentally leaks it to a global scope."""
    temp_object = LeakedEnterprisePayload("Transaction-99X")
    
    # CRITICAL LEAK: We meant to delete this, but we accidentally appended it to a persistent cache
    _hidden_rogue_cache['ghost_reference'] = temp_object
    print("  [Transaction] Data processed. Local variable 'temp_object' theoretically destroyed.")

# --- Execution Environment ---

execute_vulnerable_transaction()

# 2. The Forensics Hunt
print("\n--- Initiating Memory Sweep ---")
# We force the garbage collector to run, hoping it cleans up the object. It won't.
gc.collect()

# We scan the entire RAM for instances of our leaked class
leaked_objects = [obj for obj in gc.get_objects() if isinstance(obj, LeakedEnterprisePayload)]

if not leaked_objects:
    print("  [System] RAM is clean.")
    sys.exit()

print(f"  [ALERT] {len(leaked_objects)} leaked objects detected in RAM!")
target_leak = leaked_objects[0]

print("\n--- Executing Reverse-Pointer Traversal ---")
# THE MAGIC: We ask the CPython interpreter exactly WHO is holding onto this specific memory address.
referrers = gc.get_referrers(target_leak)

print(f"Tracking references for Object ID: {hex(id(target_leak))}")

for i, referrer in enumerate(referrers):
    # We ignore the local execution frame of this forensics loop
    if isinstance(referrer, frame.__class__ if 'frame' in locals() else type(sys._getframe())):
        continue
        
    print(f"\n  [Forensic Trace {i+1}] Pointer Origin Detected:")
    print(f"    -> Type of holding structure: {type(referrer)}")
    
    # If the referrer is a dictionary, we can find the exact key holding the object
    if isinstance(referrer, dict):
        for key, value in referrer.items():
            if value is target_leak:
                print(f"    -> MATHEMATICAL MATCH ISOLATED: Stored under dictionary key '{key}'")
                if key == 'ghost_reference':
                    print("    -> CONCLUSION: The object is trapped inside '_hidden_rogue_cache'.")

print("\nStatus: Python fundamentals verified. Rogue memory references mathematically traced and isolated via GC backward mapping.")