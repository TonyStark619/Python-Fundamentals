# Day 24: Train/Test Split - Preparing Data for AI Models

# Simulating a dataset of 10 items (e.g., 10 images or 10 rows of text)
dataset = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

# A standard AI split is 80% for training, 20% for testing
split_index = int(len(dataset) * 0.8)

# Using Python list slicing to cleanly divide the data
train_data = dataset[:split_index]
test_data = dataset[split_index:]

print("--- AI Dataset Pipeline ---")
print(f"Total Records: {len(dataset)}")
print(f"Training Data (80%): {train_data}")
print(f"Testing Data  (20%): {test_data}")