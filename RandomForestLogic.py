# Phase 2, Day 9: Ensemble Learning (Voting AI)
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Simulating placement data
# Features: [Aptitude Score, Technical Interview Score]
X_train = np.array([
    [55, 60], [70, 85], [90, 95], [40, 50], [80, 75], [85, 90]
])

# Target Label: 0 = Rejected, 1 = Selected
y_train = np.array([0, 1, 1, 0, 1, 1])

print("--- Booting Random Forest Architecture ---")

# Initialize the Model
# n_estimators=100 means we are building 100 distinct Decision Trees to vote on the outcome
ai_model = RandomForestClassifier(n_estimators=100, max_depth=4, random_state=42)

# Train the Forest
ai_model.fit(X_train, y_train)
print("100 Decision Trees generated. Voting weights optimized.\n")

# AI Inference (Testing on new candidate profiles)
# Candidate A: 65 Aptitude, 70 Technical | Candidate B: 95 Aptitude, 40 Technical
X_unseen = np.array([[65, 70], [95, 40]])
predictions = ai_model.predict(X_unseen)
probabilities = ai_model.predict_proba(X_unseen)

print("--- AI Ensemble Inference Results ---")
for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
    status = "Selected" if pred == 1 else "Rejected"
    # The confidence is literally the percentage of trees that voted for this outcome
    confidence = prob[pred] * 100 
    print(f"Candidate {i+1}: {status} (Forest Consensus: {confidence:.1f}%)")