# Day 30: The Complete AI Model Architecture

class SimpleNeuralNet:
    def __init__(self):
        # The model starts with a completely random, ignorant assumption
        self.weight = 0.5  

    def predict(self, x):
        """The Forward Pass"""
        return x * self.weight

    def train(self, inputs, targets, learning_rate=0.01, epochs=100):
        """The AI Training Loop using Gradient Descent"""
        print("--- Booting Neural Network Training ---")
        for epoch in range(1, epochs + 1):
            for x, y_true in zip(inputs, targets):
                y_pred = self.predict(x)
                
                # Calculate Error and Update Weight
                error = y_pred - y_true
                self.weight -= learning_rate * error * x
                
            if epoch % 20 == 0 or epoch == 1:
                print(f"Epoch {epoch:3} | Current Internal Weight: {self.weight:.4f}")

# The AI needs to learn to double a number (Target weight = 2.0)
dataset_inputs = [1, 2, 3, 4]
dataset_targets = [2.0, 4.0, 6.0, 8.0]

# Instantiate and train your CSE-AI model
ai_model = SimpleNeuralNet()
ai_model.train(dataset_inputs, dataset_targets)

# Testing the model on unseen data
print("\n--- Testing Model on Unseen Data ---")
unseen_input = 10
print(f"Prediction for input {unseen_input}: {ai_model.predict(unseen_input):.2f} (Target is ~20.00)")