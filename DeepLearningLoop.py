# Phase 2, Day 18: The Complete PyTorch Training Cycle
import torch
import torch.nn as nn
import torch.optim as optim

print("--- Booting Deep Learning Training Sequence ---")

# 1. Define the Dataset (Rule: y = x1 + x2)
# Features: [Logic Score, DSA Score] -> Target: Combined Metric
X_train = torch.tensor([[10.0, 20.0], [30.0, 40.0], [50.0, 10.0], [20.0, 30.0]])
y_train = torch.tensor([[30.0], [70.0], [60.0], [50.0]])

# 2. Define the Brain (A single dense layer)
class LinearPredictor(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer = nn.Linear(in_features=2, out_features=1)
    
    def forward(self, x):
        return self.layer(x)

ai_model = LinearPredictor()

# 3. Define the Engine
criterion = nn.MSELoss()
optimizer = optim.SGD(ai_model.parameters(), lr=0.0001)

epochs = 500

print("\nExecuting Training Loop...")
for epoch in range(1, epochs + 1):
    # Step A: Forward Pass
    predictions = ai_model(X_train)
    
    # Step B: Calculate Loss
    loss = criterion(predictions, y_train)
    
    # Step C: Reset Gradients, Backward Pass, Optimize
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    
    # Log progress every 100 epochs
    if epoch % 100 == 0:
        print(f"Epoch [{epoch:3}/{epochs}] | AI Error (Loss): {loss.item():.4f}")

print("\n--- Training Complete ---")
print("Validating AI on Unseen Data:")

# Test: 40 + 40 should equal roughly 80
unseen_data = torch.tensor([[40.0, 40.0]])
final_prediction = ai_model(unseen_data)
print(f"Input: [40, 40] | AI Prediction: {final_prediction.item():.2f}")