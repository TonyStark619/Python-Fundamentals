# Phase 3, Day 179: Python Fundamentals - Garbage Collection & Memory Graphing
import gc
import sys

print("--- Booting Python Memory Forensics Engine ---")

# 1. The Vulnerable Architecture
class DataNode:
    def __init__(self, name):
        self.name = name
        self.connection = None
        
    def __repr__(self):
        return f"<DataNode: {self.name}>"

# 2. Disable automatic garbage collection to freeze the memory state for forensics
gc.disable()

# 3. Create the Memory Leak (Circular Reference)
node_a = DataNode("Alpha")
node_b = DataNode("Beta")
node_a.connection = node_b
node_b.connection = node_a

print("\n[System] Simulating memory loss. Destroying hard variables...")
# We delete the variables from the global scope, but they still point to each other in RAM!
alpha_id = id(node_a)
beta_id = id(node_b)
del node_a
del node_b

# 4. The Forensics Engine
print("\n--- Executing CPython RAM Sweep ---")
# Force the garbage collector to find the ghost objects
ghost_objects_found = gc.collect()
print(f"  [GC] Garbage Collector identified {ghost_objects_found} unreachable ghost objects.")

print("\n--- Mapping the Object Reference Graph ---")
# We scan all objects currently alive in RAM
for obj in gc.get_objects():
    # If the memory address matches the variables we thought we deleted...
    if id(obj) in (alpha_id, beta_id):
        print(f"\n[Leak Detected] Object still alive in RAM: {obj}")
        
        # THE MAGIC: gc.get_referents() shows what this object is pointing TO
        referents = gc.get_referents(obj)
        for ref in referents:
            if isinstance(ref, DataNode):
                print(f"  -> Is holding a reference TO: {ref}")
                
        # THE MAGIC: gc.get_referrers() shows what is pointing AT this object
        referrers = gc.get_referrers(obj)
        for ref in referrers:
            if isinstance(ref, dict) and 'connection' in ref:
                print(f"  <- Is being held hostage BY a dictionary reference.")

print("\n[System] Re-enabling automatic garbage collection...")
gc.enable()

print("\nStatus: Python fundamentals verified. Hidden circular memory leak successfully mapped and isolated via object reference graphing.")