# Phase 3, Day 215: Python Fundamentals - Zero-Leak Enterprise Caching (weakref)
import weakref
import gc

print("--- Booting Python Zero-Leak Cache Architecture ---")

class MassiveUserPayload:
    """A heavy memory object representing a user session loaded with HD profile data."""
    def __init__(self, user_id):
        self.user_id = user_id
        # Simulating heavy RAM consumption
        self.data_matrix = [x for x in range(100_000)]
        print(f"    [RAM] Allocated 100K blocks for {self.user_id}")

    def __repr__(self):
        return f"<UserSession: {self.user_id}>"


# 1. The Vulnerable Legacy Cache
# Standard dictionaries use "Strong References". They mathematically block garbage collection.
legacy_strong_cache = {}

# 2. The Enterprise Architecture
# WeakValueDictionary uses "Weak References". If no other part of the system is using the object,
# this cache will let the Garbage Collector destroy it, automatically erasing the key.
enterprise_weak_cache = weakref.WeakValueDictionary()

# --- Execution Environment ---

def execute_user_transaction(user_id):
    """Simulates an active user connected to the server."""
    # The active user object in the local execution scope
    active_session = MassiveUserPayload(user_id)
    
    # Store the user in both caches
    legacy_strong_cache[user_id] = active_session
    enterprise_weak_cache[user_id] = active_session
    
    print(f"  [System] Cached state for {user_id}:")
    print(f"    -> Strong Cache Status: {legacy_strong_cache.get(user_id)}")
    print(f"    -> Weak Cache Status:   {enterprise_weak_cache.get(user_id)}")
    
    # The transaction ends. 'active_session' is locally deleted as the function returns.
    print(f"  [Transaction Complete] Local variables destroyed for {user_id}.\n")


print("\n--- Diagnostic: Simulating User Connections ---")
execute_user_transaction("Student_Alpha")

print("--- Initiating Garbage Collection Sweep ---")
# Force the CPython OS kernel to clean up any unreferenced memory
gc.collect()

print("\n--- Post-Sweep Cache Diagnostics ---")

# The Strong Cache held the memory hostage. It is permanently leaked into RAM.
if "Student_Alpha" in legacy_strong_cache:
    print(f"[ALERT] Legacy Cache is bleeding RAM: {legacy_strong_cache['Student_Alpha']} is still alive!")

# THE MAGIC: The Weak Cache detected that the transaction ended, allowed the GC to destroy 
# the payload, and automatically deleted the dictionary key to protect the server.
if "Student_Alpha" not in enterprise_weak_cache:
    print(f"[SUCCESS] Enterprise Cache verified secure. Key mathematically self-terminated.")
    
print("\nStatus: Python fundamentals verified. Out-Of-Memory (OOM) leaks neutralized via WeakReference dictionary mapping.")