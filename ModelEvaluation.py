# Phase 2, Day 11: AI Pipeline Evaluation Metrics
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np

# Simulating 10 actual placement outcomes vs what our AI predicted
# 1 = Placed in a top-tier MNC, 0 = Not Placed
y_actual = np.array([1, 1, 0, 1, 0, 0, 1, 0, 1, 1])
y_predict = np.array([1, 1, 0, 0, 0, 1, 1, 0, 1, 1]) # Missed one, false positive on another

print("--- Booting Model Evaluation Protocol ---")

# 1. Generate the Confusion Matrix
# Matrix layout: [[True Negatives, False Positives], [False Negatives, True Positives]]
matrix = confusion_matrix(y_actual, y_predict)
print("Confusion Matrix Layout:")
print(matrix)

print("\n--- Detailed Classification Metrics ---")
# 2. Generate Precision, Recall, and F1-Score reports
# Precision: Out of all predicted positive cases, how many were actually positive?
# Recall: Out of all actual positive cases, how many did the AI successfully catch?
report = classification_report(y_actual, y_predict, target_names=["Not Placed", "Placed"])
print(report)