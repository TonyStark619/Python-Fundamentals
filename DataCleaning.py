# Phase 2, Day 4: Handling Missing Data in AI Pipelines
import pandas as pd
import numpy as np

# Simulating a dirty real-world dataset with missing values (NaN)
raw_data = {
    "Feature_Pixels": [255, 128, np.nan, 200, 10],
    "Feature_Audio": [1.2, np.nan, 3.4, 2.1, np.nan],
    "Target_Label": ["Cat", "Dog", "Dog", "Cat", "Bird"]
}

df = pd.DataFrame(raw_data)
print("--- Raw Database Extraction (Dirty) ---")
print(df)

print("\n--- Initializing AI Data Cleaning Protocol ---")

# Strategy: Imputation (Filling missing data with the column mean)
# This prevents us from losing valuable training rows.
clean_df = df.copy()

# Fill empty pixel rows with the average pixel value
clean_df["Feature_Pixels"] = clean_df["Feature_Pixels"].fillna(clean_df["Feature_Pixels"].mean())

# Fill empty audio rows with the average audio frequency
clean_df["Feature_Audio"] = clean_df["Feature_Audio"].fillna(clean_df["Feature_Audio"].mean())

print("Missing values successfully imputed using statistical means.\n")
print("--- Cleaned DataFrame (Ready for Tensor Conversion) ---")
print(clean_df)