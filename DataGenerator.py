# Day 19: Generators - Memory efficient AI data processing

def batch_generator(data, batch_size):
    """Yields chunks of data one at a time instead of storing all in memory."""
    for i in range(0, len(data), batch_size):
        # 'yield' pauses the function and sends the batch out
        yield data[i : i + batch_size]

# Simulating 10,000 rows of raw dataset
massive_dataset = list(range(1, 10001))

print("--- AI Training: Streaming Data Batches ---")

# Create the generator object (No data is actually processed yet)
data_stream = batch_generator(massive_dataset, batch_size=2000)

# Pulling the first two batches into memory one at a time using next()
print(f"Batch 1 Loaded: {next(data_stream)[:5]} ... (2000 items)")
print(f"Batch 2 Loaded: {next(data_stream)[:5]} ... (2000 items)")