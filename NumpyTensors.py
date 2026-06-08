# Phase 2, Day 1: Transitioning to Industry Standards
import numpy as np

# A standard list you used in Phase 1
raw_data = [1.2, 2.5, 3.8, 4.1]

# Converting the list into a highly optimized NumPy Tensor
tensor_1d = np.array(raw_data)

print("--- AI Data Pipeline: NumPy Initialization ---")
print(f"Standard Python List: {raw_data}")
print(f"NumPy Tensor:         {tensor_1d}")

# Vectorized Math: 
# Notice there is no 'for' loop. NumPy multiplies every element in memory instantly.
optimized_math = tensor_1d * 2.0

print(f"\nVectorized Output (x2): {optimized_math}")
print("Status: Core tensor library initialized successfully.")