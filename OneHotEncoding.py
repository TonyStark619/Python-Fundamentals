# Phase 2, Day 6: Translating Text to Tensors for AI Models
import pandas as pd

# Simulating a dataset with text categories
raw_data = {
    "Transaction_ID": [101, 102, 103, 104],
    "User_Device": ["Mobile", "Desktop", "Tablet", "Mobile"],
    "Time_Spent_Min": [12, 45, 8, 22]
}

df = pd.DataFrame(raw_data)
print("--- Raw Feature Matrix (Pre-Encoding) ---")
print(df)

print("\n--- Initializing One-Hot Encoding Protocol ---")

# get_dummies automatically finds categorical columns and splits them into binary tensors
# dtype=int ensures we get 0s and 1s instead of True/False
encoded_df = pd.get_dummies(df, columns=["User_Device"], dtype=int)

print("Categorical text successfully converted to mathematical binary columns.\n")
print("--- Encoded Matrix (Ready for Neural Network Input) ---")
print(encoded_df)