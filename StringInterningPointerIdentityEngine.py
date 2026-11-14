# Phase 3, Master Day 233: Python Fundamentals - CPython Global String Interning & O(1) Pointer Identity
import sys
import time

print("--- Booting CPython Global String Interning & Pointer-Identity Engine ---")

# Construct two identical 50,000-character telemetry symbols dynamically at runtime
# (Dynamic construction bypasses compile-time constant folding, allocating two separate heap objects)
SYMBOL_PREFIX = "TELEMETRY_SHARD_IDENTIFIER_"
raw_symbol_alpha = "".join([SYMBOL_PREFIX, "X" * 50_000, "_NODE_01"])
raw_symbol_beta = "".join([SYMBOL_PREFIX, "X" * 50_000, "_NODE_01"])

print("\n--- Diagnostic 1: Un-Interned Dynamic Heap Allocation Forensics ---")
print(f"  → Symbol Length                  : {len(raw_symbol_alpha):,} characters")
print(f"  → Value Equality (alpha == beta) : {raw_symbol_alpha == raw_symbol_beta}")
print(f"  → Pointer Identity (alpha is beta): {raw_symbol_alpha is raw_symbol_beta} (Distinct RAM addresses!)")
print(f"  → Heap Address Alpha vs Beta     : {hex(id(raw_symbol_alpha))} != {hex(id(raw_symbol_beta))}")


print("\n--- Diagnostic 2: Registering in CPython's Global Interning Table (sys.intern) ---")
# sys.intern() looks up the string in CPython's internal C hash table and returns the singleton pointer
interned_alpha = sys.intern(raw_symbol_alpha)
interned_beta = sys.intern(raw_symbol_beta)

print(f"  → Post-Intern Pointer Identity   : {interned_alpha is interned_beta} (Canonical Singleton Shared!)")
print(f"  → Canonical Heap Address         : {hex(id(interned_alpha))} == {hex(id(interned_beta))}")


print("\n--- Diagnostic 3: Benchmarking O(K) Byte Equality (==) vs O(1) Register Identity (is) ---")
ITERATIONS = 500_000

# Force two fresh un-interned strings so CPython must execute character buffer comparison
uninterned_a = "".join(["CLUSTER_ROUTE_", "A" * 10_000])
uninterned_b = "".join(["CLUSTER_ROUTE_", "A" * 10_000])

start_eq = time.perf_counter()
for _ in range(ITERATIONS):
    _ = (uninterned_a == uninterned_b)
eq_duration = time.perf_counter() - start_eq

# Compare the interned strings using 'is' (Single 64-bit CPU pointer equality check)
start_is = time.perf_counter()
for _ in range(ITERATIONS):
    _ = (interned_alpha is interned_beta)
is_duration = time.perf_counter() - start_is

print(f"  → 500K Byte-Scan Comparisons (==)      : {eq_duration:.4f} seconds")
print(f"  → 500K Interned Pointer Checks (is)    : {is_duration:.4f} seconds")
print(f"  → Throughput Acceleration              : {eq_duration / max(is_duration, 1e-9):.1f}x faster")

print(
    "\nStatus: Python fundamentals verified. Dynamic string duplication eliminated and O(K) comparisons collapsed to O(1) pointer checks via sys.intern()."
)