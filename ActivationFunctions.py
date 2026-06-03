import math

# Day 26: Activation Functions - How Neural Networks "Think"

def relu(x):
    """Rectified Linear Unit: Kills negative signals, passes positive ones."""
    return max(0, x)

def sigmoid(x):
    """Sigmoid: Squashes any number into a probability range between 0.0 and 1.0."""
    return 1 / (1 + math.exp(-x))

# Simulating raw mathematical outputs (logits) from a neural network layer
raw_signals = [-2.5, 0.0, 1.2, 3.5]

print("--- AI Activation Layer Outputs ---")
for signal in raw_signals:
    print(f"Raw Signal: {signal:4.1f} | ReLU: {relu(signal):4.1f} | Sigmoid: {sigmoid(signal):.4f}")