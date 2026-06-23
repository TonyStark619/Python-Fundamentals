# Phase 2, Day 15: PyTorch Automatic Differentiation
import torch

print("--- Booting PyTorch Autograd Engine ---")

# We create tensors and set requires_grad=True. 
# This tells PyTorch: "Watch everything that happens to these numbers."
x = torch.tensor(2.0, requires_grad=True) # Input data
w = torch.tensor(3.0, requires_grad=True) # Neuron Weight
b = torch.tensor(1.0, requires_grad=True) # Neuron Bias

# Step 1: The Forward Pass (Linear Equation: y = w*x + b)
# Under the hood, PyTorch is building a dynamic computational graph
y = w * x + b
print(f"Forward Pass Output (Prediction): {y.item()}")

# Step 2: The Backward Pass
# This single command instantly calculates the calculus derivatives for w, x, and b
y.backward()

print("\n--- Gradient Analysis (Derivatives Calculated Instantly) ---")
# Gradient of y with respect to w (dy/dw = x)
print(f"Gradient of Weight (dy/dw): {w.grad.item():.1f}")

# Gradient of y with respect to b (dy/db = 1)
print(f"Gradient of Bias (dy/db):   {b.grad.item():.1f}")

print("\nStatus: Autograd executed successfully. Manual calculus obsolete.")