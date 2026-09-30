# Phase 3, Day 183: Python Fundamentals - Live Bytecode Hot-Swapping (__code__)

print("--- Booting Python Compiler-Level Logic Override ---")

# 1. The original, broken function running in production
def calculate_tax(revenue: float):
    """Calculates a 20% corporate tax rate."""
    print("  [Module] Executing Legacy Tax Engine...")
    # CRITICAL BUG: It is dividing instead of multiplying!
    return revenue / 0.20 

# 2. The patched logic we want to inject
def patched_tax_engine(revenue: float):
    print("  [Module] Executing Patched Tax Engine...")
    return revenue * 0.20

# --- Execution Environment ---

print("\n--- Scenario 1: Executing Original State ---")
revenue_stream = 1000.0
print(f"Target Revenue: {revenue_stream}")
print(f"Result: {calculate_tax(revenue_stream)}") # Will return a wildly incorrect 5000.0

print("\n[System] Initiating C-Level Bytecode Hot-Swap...")
# THE MAGIC: We literally overwrite the compiled binary code of the broken function
# The function name remains 'calculate_tax', but its brain is now 'patched_tax_engine'
calculate_tax.__code__ = patched_tax_engine.__code__
print("  -> Bytecode injection successful. Memory address retained.")

print("\n--- Scenario 2: Executing Hot-Swapped State ---")
print(f"Target Revenue: {revenue_stream}")
# We call the exact same function name, but the logic has been completely hijacked
print(f"Result: {calculate_tax(revenue_stream)}") # Will correctly return 200.0

print("\nStatus: Python fundamentals verified. Function bytecode successfully overwritten at runtime without redeployment.")