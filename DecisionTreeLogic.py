# Phase 2, Day 8: Non-Linear Machine Learning
from sklearn.tree import DecisionTreeClassifier
import numpy as np

# Simulating candidate data for a 50 LPA MNC role
# Features: [CGPA, DSA_Problems_Solved]
X_train = np.array([
    [6.5, 50],   # Candidate 1
    [7.2, 120],  # Candidate 2
    [8.5, 300],  # Candidate 3
    [9.1, 450],  # Candidate 4
    [5.8, 10]    # Candidate 5
])

# Target Label: 0 = Rejected, 1 = Hired
y_train = np.array([0, 0, 1, 1, 0])

print("--- Booting Decision Tree Classifier ---")

# Initialize the Model
# max_depth prevents the tree from overthinking and memorizing the data
ai_model = DecisionTreeClassifier(max_depth=3, random_state=42)

# Train the Model
ai_model.fit(X_train, y_train)
print("Decision Tree mapped. Node splits calculated successfully.\n")

# AI Inference (Testing on new students)
# Test 1: 7.8 CGPA, 250 Problems | Test 2: 6.9 CGPA, 400 Problems
X_unseen = np.array([[7.8, 250], [6.9, 400]])
predictions = ai_model.predict(X_unseen)

print("--- AI Inference Results ---")
for i, pred in enumerate(predictions):
    status = "Hired" if pred == 1 else "Rejected"
    print(f"Unseen Candidate {i+1} Prediction: {status}")