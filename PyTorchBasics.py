# Phase 2, Day 14: Welcome to Deep Learning
import torch
import numpy as np

print("--- Booting PyTorch Neural Architecture ---")

# 1. From standard Python/NumPy to PyTorch Tensors
raw_list = [[1.0, 2.0], [3.0, 4.0]]
np_array = np.array(raw_list)

# Converting to a PyTorch Tensor
tensor = torch.tensor(raw_list)

print("Standard NumPy Array:")
print(np_array)
print("\nPyTorch Tensor:")
print(tensor)
print(f"Data Type: {tensor.dtype} | Architecture Shape: {tensor.shape}")

print("\n--- Initializing Tensor Operations ---")
# PyTorch allows for instantaneous, highly optimized matrix mathematics
multiplier_tensor = torch.tensor([[2.0, 0.0], [0.0, 2.0]])

# Matrix Multiplication (The core math behind every Neural Network)
result_tensor = torch.matmul(tensor, multiplier_tensor)
print("Matrix Multiplication Output:")
print(result_tensor)

print("\n--- Hardware Acceleration Diagnostics ---")
# Checking if a GPU is available to accelerate AI training
if torch.cuda.is_available():
    print("Status: NVIDIA CUDA GPU detected. System ready for heavy deep learning.")
elif torch.backends.mps.is_available():
    print("Status: Apple Silicon GPU detected. System ready.")
else:
    print("Status: GPU not detected. Defaulting to CPU processing.")