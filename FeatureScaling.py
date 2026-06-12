# Phase 2, Day 5: Min-Max Normalization for AI Feature Matrices
import pandas as pd

# Data from yesterday's pipeline, now clean and ready for scaling
cleaned_features = {
    "Feature_Pixels": [255, 128, 198, 200, 10],
    "Feature_Audio_Hz": [1200, 44100, 22000, 8000, 1500] # Massive range disparity!
}

df = pd.DataFrame(cleaned_features)
print("--- Raw Features (Before Scaling) ---")
print(df)

print("\n--- Initializing Min-Max Normalization Protocol ---")
# Mathematical Formula: (x - min) / (max - min)
scaled_df = df.copy()

for column in scaled_df.columns:
    col_min = scaled_df[column].min()
    col_max = scaled_df[column].max()
    # Vectorized execution across columns
    scaled_df[column] = (scaled_df[column] - col_min) / (col_max - col_min)

print("Features mapped to unified scale matrix [0.0, 1.0] instantly.\n")
print("--- Normalized DataFrame (Ready for Tensor Processing) ---")
print(scaled_df)