# Day 25: Mean Squared Error (MSE) - The AI Loss Function

# Simulating what the AI predicted vs the actual correct answers
actual_labels = [100, 150, 200, 250]
ai_predictions = [110, 140, 210, 240]

print("--- AI Model Evaluation ---")

# Step 1: Calculate the squared difference for each pair using zip()
# We square it so negative errors don't cancel out positive ones
squared_errors = [(actual - pred) ** 2 for actual, pred in zip(actual_labels, ai_predictions)]
print(f"Individual Squared Errors: {squared_errors}")

# Step 2: Find the average (mean) of those squared errors
mse = sum(squared_errors) / len(actual_labels)

print(f"Mean Squared Error (Loss): {mse}")
print("Status: The lower the MSE, the smarter the AI.")