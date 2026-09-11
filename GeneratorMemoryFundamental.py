# Phase 3, Day 46: Python Fundamentals - Generators & Memory Optimization
import sys

print("--- Booting Python Fundamental Memory Diagnostics ---")

# 1. The Standard List (RAM Heavy)
def naive_data_loader(limit):
    """Loads everything into memory simultaneously."""
    dataset = []
    for i in range(limit):
        dataset.append(i ** 2)
    return dataset

# 2. The Python Generator (RAM Efficient)
def optimized_data_generator(limit):
    """Yields one item at a time. Pauses execution between calls."""
    for i in range(limit):
        yield i ** 2

# --- Execution Environment ---
massive_limit = 5_000_000

print(f"\n[System] Initiating payload generation for {massive_limit} integers...")

# Generate using a standard list
list_payload = naive_data_loader(massive_limit)
list_memory_mb = sys.getsizeof(list_payload) / (1024 * 1024)

# Generate using a Python Generator
generator_payload = optimized_data_generator(massive_limit)
generator_memory_bytes = sys.getsizeof(generator_payload)

print("\n--- Memory Consumption Report ---")
print(f"Standard Python List RAM Usage:   {list_memory_mb:.2f} MB")
print(f"Python Generator RAM Usage:       {generator_memory_bytes} BYTES")

print("\n[Diagnostic Test] Streaming the first 3 values from the generator:")
for index, value in enumerate(generator_payload):
    if index >= 3:
        break
    print(f" -> Value: {value}")

print("\nStatus: Python fundamentals verified. Infinite data streaming achieved with O(1) memory overhead.")