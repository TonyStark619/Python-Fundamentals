# Phase 2, Day 17: PyTorch Loss and Optimization Engine
import torch
import torch.nn as nn
import torch.optim as optim

print("--- Booting Deep Learning Training Engine ---")

# 1. Rebuilding a micro-version of yesterday's architecture
model = nn.Linear(in_features=1, out_features=1)

# 2. Defining the Engine
# Loss Function: Mean Squared Error (Calculates how far off the prediction was)
criterion = nn.MSELoss()

# Optimizer: Stochastic Gradient Descent (Adjusts the weights to fix the error)
# lr = Learning Rate (How drastically it changes its mind after a mistake)
optimizer = optim.SGD(model.parameters(), lr=0.01)

# 3. Simulating a training scenario (Rule: y = x * 2.0)
input_data = torch.tensor([[1.0], [2.0], [3.0]])
target_data = torch.tensor([[2.0], [4.0], [6.0]])

print("\nExecuting Single Training Step...")

# Step A: Forward Pass (AI makes a guess)
predictions = model(input_data)

# Step B: Calculate Error
loss = criterion(predictions, target_data)
print(f"Mathematical Error (Loss): {loss.item():.4f}")

# Step C: Reset Old Gradients (Crucial PyTorch step to avoid compounding errors)
optimizer.zero_grad()

# Step D: Backward Pass (Calculate the calculus for the required fix)
loss.backward()

# Step E: Optimize (Update the weights automatically)
optimizer.step()

print("Status: Weights and biases successfully optimized using SGD.")