# Day 28: Gradient Descent - How an AI Learns

# Initial state of our AI neuron
weight = 0.5
input_data = 2.0
target_answer = 1.0  # What the AI *should* output
learning_rate = 0.1  # How fast the AI updates its internal logic

print("--- AI Training: Weight Optimization ---")
print(f"Initial Weight: {weight}")

# Step 1: Forward Pass (The AI makes a prediction)
prediction = input_data * weight

# Step 2: Calculate the Error
error = prediction - target_answer

# Step 3: Gradient Descent (The Update Rule)
# Nudging the weight in the opposite direction of the error
weight_update = learning_rate * error * input_data
new_weight = weight - weight_update

print(f"Prediction: {prediction:.2f} | Target: {target_answer:.2f} | Error: {error:.2f}")
print(f"Updated Weight: {new_weight:.4f}")
print("Status: The AI has successfully adjusted its weight based on its mistake.")