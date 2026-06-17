# Phase 2, Day 10: Unsupervised Machine Learning
from sklearn.cluster import KMeans
import numpy as np

# Simulating raw customer behavior data (NO LABELS)
# Features: [Time Spent on App (mins), Money Spent ($)]
X_train = np.array([
    [15, 20],  [18, 22],  [12, 18],  # Group A (Low engagement)
    [85, 120], [90, 115], [88, 130]  # Group B (High engagement)
])

print("--- Booting Unsupervised AI Architecture ---")

# Initialize the Model
# We tell the AI to look for 2 distinct clusters in the chaos
ai_model = KMeans(n_clusters=2, random_state=42, n_init=10)

# Train the Model (Notice there is no 'y_train' passed in)
ai_model.fit(X_train)
print("Data points analyzed. Mathematical clusters successfully identified.\n")

# AI Inference (Testing on new, unknown users)
# User 1: 20 mins, $25 | User 2: 95 mins, $140
X_unseen = np.array([[20, 25], [95, 140]])
predictions = ai_model.predict(X_unseen)

print("--- AI Clustering Results ---")
for i, pred in enumerate(predictions):
    # The AI assigns them to Cluster 0 or Cluster 1 based on its own logic
    print(f"Unknown User {i+1} assigned to: Cluster {pred}")

print("\nInternal Centroids (The exact center of each cluster):")
print(ai_model.cluster_centers_)