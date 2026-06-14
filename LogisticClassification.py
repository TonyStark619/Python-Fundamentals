# Phase 2, Day 7: Industry Standard ML with Scikit-Learn
from sklearn.linear_model import LogisticRegression
import numpy as np

# Simulating a clean, numerical dataset (e.g., predicting placement success)
# Features: [Hours Studied per Day, DSA Problems Solved]
X_train = np.array([[1, 10], [2, 20], [4, 50], [5, 70], [6, 90]])

# Target Label: 0 = Failed Interview, 1 = Cleared Interview
y_train = np.array([0, 0, 1, 1, 1])

print("--- Booting Scikit-Learn ML Pipeline ---")

# 1. Initialize the Model (Binary Classification)
ai_model = LogisticRegression()

# 2. Train the Model instantly (This replaces the manual math loops)
ai_model.fit(X_train, y_train)
print("Model Training Complete. Weights and biases optimized.\n")

# 3. AI Inference (Predicting on unseen student data)
# Student A: 3 hours, 30 problems. Student B: 5 hours, 80 problems.
X_unseen = np.array([[3, 30], [5, 80]])
predictions = ai_model.predict(X_unseen)
probabilities = ai_model.predict_proba(X_unseen)

print("--- AI Inference Results ---")
for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    status = "Cleared" if pred == 1 else "Failed"
    # Extract the probability of the predicted class
    confidence = prob[pred] * 100 
    print(f"Candidate {i+1} Prediction: {status} (Confidence: {confidence:.1f}%)")