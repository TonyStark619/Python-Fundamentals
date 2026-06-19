# Phase 2, Day 12: K-Fold Cross-Validation for AI Reliability
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Simulating 20 candidates for a placement prediction dataset
# Features: [Aptitude Score, Interview Score]
np.random.seed(42)
X_data = np.random.randint(40, 100, size=(20, 2))

# Target: 1 = Placed, 0 = Not Placed (Simulating a pattern based on scores)
y_data = np.array([1 if x[0] + x[1] > 140 else 0 for x in X_data])

print("--- Booting K-Fold Cross-Validation Protocol ---")

# Initialize our AI Architecture
ai_model = RandomForestClassifier(n_estimators=50, random_state=42)

# Execute 5-Fold Cross Validation
# The dataset is split into 5 pieces. The model trains on 4, tests on 1.
# It repeats this process 5 times, rotating the test piece each time.
cv_scores = cross_val_score(ai_model, X_data, y_data, cv=5)

print("\nExecuting 5 distinct training and evaluation cycles...")
for i, score in enumerate(cv_scores, start=1):
    print(f"Cycle {i} Accuracy: {score * 100:.1f}%")

# The true measure of the AI's intelligence is the average
mean_accuracy = cv_scores.mean() * 100
print(f"\n--- Final Model Diagnostics ---")
print(f"Validated True Accuracy: {mean_accuracy:.1f}%")
print("Status: Model evaluated with extreme rigor. No 'lucky' test splits.")