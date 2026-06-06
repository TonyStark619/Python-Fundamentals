# Day 29: The Complete AI Training Loop

# Initial state (The AI starts with a random, incorrect assumption)
weight = 0.5  
learning_rate = 0.01
epochs = 100

# Training Dataset (The rule is y = x * 2.5)
inputs = [1, 2, 3, 4]
targets = [2.5, 5.0, 7.5, 10.0]

print("--- Initiating AI Training Sequence ---")

# Training over multiple iterations (epochs)
for epoch in range(1, epochs + 1):
    total_error = 0
    
    for x, y_true in zip(inputs, targets):
        # 1. Forward Pass (Prediction)
        y_pred = x * weight
        
        # 2. Calculate Loss (Error)
        error = y_pred - y_true
        total_error += error ** 2  
        
        # 3. Gradient Descent (Weight Update)
        weight_update = learning_rate * error * x
        weight -= weight_update
    
    # Log the AI's learning progress every 20 epochs
    if epoch % 20 == 0 or epoch == 1:
        avg_mse = total_error / len(inputs)
        print(f"Epoch {epoch:3} | MSE (Loss): {avg_mse:.4f} | Current Weight: {weight:.4f}")

print("\nTraining Complete.")
print(f"Final learned weight: {weight:.4f} (Target was 2.5)")