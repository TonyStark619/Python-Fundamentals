# Day 11: Using Built-in Modules (Random)
import random

# AI models require random weight initialization before training
# Simulating random weights between -1.0 and 1.0 for a basic neural network layer
weights = [random.uniform(-1.0, 1.0) for _ in range(3)]

print("Initialized AI Model Weights:")
for i, w in enumerate(weights):
    print(f"Neuron {i+1}: {w:.4f}")