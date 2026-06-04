# Day 27: The Forward Pass - Simulating a Neural Network Layer

def relu(x):
    """Activation Function: Kills negative signals, passes positive ones."""
    return max(0, x)

# Simulating a single neuron receiving inputs from 3 previous nodes
inputs = [1.2, 0.5, -1.0]
weights = [0.8, -0.4, 0.5]
bias = 0.1

print("--- AI Architecture: Forward Pass ---")

# Step 1: Dot Product (Summing the multiplied inputs and weights)
# We use zip() to perfectly pair the lists together
weighted_sum = sum(i * w for i, w in zip(inputs, weights))

# Step 2: Add the bias (The neuron's built-in offset)
logit = weighted_sum + bias

# Step 3: Pass through Activation Function
output = relu(logit)

print(f"Inputs Received:  {inputs}")
print(f"Weights Applied:  {weights}")
print(f"Raw Calculation:  {logit:.4f}")
print(f"Final Output:     {output:.4f}")