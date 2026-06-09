# Phase 2, Day 2: Tensor Dimensions and Reshaping
import numpy as np

# Simulating a raw stream of 6 pixel values (1D Tensor)
raw_pixel_stream = np.array([255, 128, 64, 0, 45, 90])

print("--- AI Pipeline: Shape Manipulation ---")
print(f"Original Data: {raw_pixel_stream}")
print(f"Original Shape: {raw_pixel_stream.shape} (1D Array)")

# Reshaping the 1D stream into a 2x3 Matrix (2D Tensor)
# The total number of elements must remain exactly the same (2 * 3 = 6)
image_matrix = raw_pixel_stream.reshape(2, 3)

print("\nReshaped 2x3 Image Matrix:")
print(image_matrix)
print(f"New Shape: {image_matrix.shape} (2D Matrix)")