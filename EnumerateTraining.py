# Day 23: enumerate() - Tracking data and indices simultaneously

# Simulating a batch of AI training data
training_batches = ["ImageSet_A", "ImageSet_B", "TextData_C", "Audio_D"]

print("--- AI Model Training Sequence ---")

# enumerate automatically provides the index (epoch) and the data
# We start the index at 1 instead of 0 for cleaner logging
for epoch, batch in enumerate(training_batches, start=1):
    print(f"Epoch {epoch}: Processing {batch}...")

print("\nTraining Complete.")