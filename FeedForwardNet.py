# Phase 2, Day 16: The PyTorch Neural Architecture
import torch
import torch.nn as nn
import torch.nn.functional as F

print("--- Booting Deep Learning Architecture ---")

# Every professional PyTorch model inherits from nn.Module
class PlacementPredictor(nn.Module):
    def __init__(self):
        super(PlacementPredictor, self).__init__()
        
        # Layer 1: Takes 2 inputs (e.g., Aptitude, DSA) and routes to 4 hidden neurons
        self.hidden_layer = nn.Linear(in_features=2, out_features=4)
        
        # Layer 2: Takes the 4 hidden signals and condenses them into 1 final output
        self.output_layer = nn.Linear(in_features=4, out_features=1)

    def forward(self, x):
        """This defines exactly how data flows through the brain."""
        # 1. Pass through hidden layer, apply ReLU to kill negative signals
        x = F.relu(self.hidden_layer(x))
        
        # 2. Pass to output layer, apply Sigmoid to squash the answer between 0 and 1
        x = torch.sigmoid(self.output_layer(x))
        return x

# Initialize the AI
ai_model = PlacementPredictor()
print("\nModel Architecture Constructed:")
print(ai_model)

print("\n--- AI Inference Diagnostics ---")
# Simulating a candidate: 85 Aptitude Score, 90 DSA Score
unseen_candidate = torch.tensor([[85.0, 90.0]])

# Pass the candidate through the AI
prediction = ai_model(unseen_candidate)

# The output is a raw tensor probability. Extract the number using .item()
confidence = prediction.item() * 100
print(f"Candidate Evaluation Complete.")
print(f"AI Selection Probability: {confidence:.2f}%")