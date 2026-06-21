# Phase 2, Day 13: Mathematical AI Optimization
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

print("--- Booting AI Hyperparameter Optimization Protocol ---")

# Simulating a dataset (e.g., student traits vs placement outcome)
# Features: [Logical_Aptitude, DSA_Score, Comm_Skills]
X_train = [
    [85, 90, 8], [60, 40, 5], [95, 85, 9], 
    [45, 50, 4], [80, 75, 7], [55, 60, 6]
]
y_train = [1, 0, 1, 0, 1, 0] # 1 = Selected, 0 = Rejected

# 1. Initialize the Base Architecture
base_model = RandomForestClassifier(random_state=42)

# 2. Define the 'Grid' of settings we want the machine to test
# It will test 10 trees vs 50 trees vs 100 trees, combined with different depth limits
search_space = {
    'n_estimators': [10, 50, 100],
    'max_depth': [None, 3, 5],
    'criterion': ['gini', 'entropy']
}

print(f"Testing {len(search_space['n_estimators']) * len(search_space['max_depth']) * len(search_space['criterion'])} unique architectural combinations...")

# 3. Execute the Grid Search (cv=3 means 3-Fold Cross Validation for every test)
optimizer = GridSearchCV(estimator=base_model, param_grid=search_space, cv=3)
optimizer.fit(X_train, y_train)

# 4. Extract the absolute best configuration
print("\n--- Optimization Complete ---")
print("Best Architectural Configuration Found:")
for param, value in optimizer.best_params_.items():
    print(f" -> {param}: {value}")

print(f"\nPeak Validated Accuracy: {optimizer.best_score_ * 100:.1f}%")