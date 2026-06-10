# Phase 2, Day 3: Structured AI Datasets with Pandas
import pandas as pd

# Simulating raw, structured data extracted from a database
ai_training_data = {
    "Feature_Pixels": [255, 128, 64, 200],
    "Feature_Audio": [1.2, 0.8, 3.4, 2.1],
    "Target_Label": ["Cat", "Dog", "Dog", "Cat"]
}

print("--- AI Data Pipeline: Loading DataFrame ---")

# Converting the dictionary into a Pandas DataFrame
df = pd.DataFrame(ai_training_data)

# Displaying the structured table (looks just like an Excel sheet)
print(df)

print("\n--- Pipeline Diagnostics ---")
# Extracting a specific column instantly
print(f"Total Labels Count:\n{df['Target_Label'].value_counts()}")

# Pandas seamlessly bridges the gap to NumPy when it's time for math
print("\nConverting Pixels to NumPy Tensor for Math...")
pixel_tensor = df['Feature_Pixels'].to_numpy()
print(f"Tensor Array: {pixel_tensor}")