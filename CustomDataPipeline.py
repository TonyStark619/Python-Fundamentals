# Phase 2, Day 19: Enterprise Production Data Pipelines
import torch
from torch.utils.data import Dataset, DataLoader

print("--- Booting PyTorch Data Pipeline Infrastructure ---")

# 1. Subclassing the native PyTorch Dataset class
class PlacementDataset(Dataset):
    def __init__(self):
        # Simulating 8 student profiles: [Aptitude Score, Coding Score]
        self.features = torch.tensor([
            [60.0, 50.0], [85.0, 90.0], [70.0, 65.0], [95.0, 95.0],
            [50.0, 40.0], [80.0, 85.0], [65.0, 75.0], [90.0, 80.0]
        ], dtype=torch.float32)
        
        # Binary target: 1 = Placed, 0 = Not Placed
        self.labels = torch.tensor([[0], [1], [0], [1], [0], [1], [0], [1]], dtype=torch.float32)

    def __len__(self):
        """Returns the absolute size of the data ledger."""
        return len(self.features)

    def __getitem__(self, index):
        """Allows the DataLoader to cleanly pull one single data row at a time."""
        return self.features[index], self.labels[index]

# Initialize our custom structural dataset
dataset = PlacementDataset()

# 2. Wrapping with the DataLoader for industry-grade batch streaming
# batch_size=2 means data streams out in tiny, manageable sets of 2 rows
# shuffle=True ensures the AI never memorizes the sequence of the dataset
data_streamer = DataLoader(dataset, batch_size=2, shuffle=True)

print(f"Dataset securely loaded. Total records: {len(dataset)}")
print("Initiating mini-batch streaming diagnostics...\n")

# Simulating exactly what happens inside a production training epoch
for epoch in range(1, 3):
    print(f"--- Streaming Epoch {epoch} ---")
    for batch_idx, (batch_features, batch_labels) in enumerate(data_streamer):
        print(f" Pack {batch_idx + 1} | Feature Matrix Shape: {list(batch_features.shape)} | Targets: {batch_labels.flatten().tolist()}")

print("\nStatus: Dynamic batch-streaming pipeline fully operational.")