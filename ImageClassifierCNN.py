# Phase 2, Day 22: End-to-End Vision Classification Architecture
import torch
import torch.nn as nn
import torch.nn.functional as F

print("--- Booting End-to-End Vision Pipeline ---")

class VisionClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        # 1. Feature Extraction (The Eyes)
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # 2. The Bridge (Flattening the 2D grid into a 1D line)
        # We calculate the flat size: 16 channels * 13 height * 13 width
        self.flat_features = 16 * 13 * 13 
        
        # 3. Decision Making (The Brain)
        self.fc1 = nn.Linear(in_features=self.flat_features, out_features=10) # 10 possible outputs (e.g., digits 0-9)

    def forward(self, x):
        # Pass through the eyes
        x = self.pool(F.relu(self.conv1(x)))
        print(f"Spatial Features Mapped: {list(x.shape)}")
        
        # Flatten the grid into a single 1D tensor stream
        x = torch.flatten(x, start_dim=1)
        print(f"Features Flattened: {list(x.shape)}")
        
        # Pass into the brain for a final decision
        x = self.fc1(x)
        return x

# Initialize the architecture
ai_model = VisionClassifier()

# Simulating one Grayscale image (28x28 pixels, like the MNIST digit dataset)
dummy_image = torch.randn(1, 1, 28, 28)

print("\nExecuting Vision Inference...")
raw_predictions = ai_model(dummy_image)

print("\n--- Model Output ---")
print(f"Raw Class Logits: {raw_predictions.detach().numpy()}")
print("Status: Image successfully translated from spatial pixels to mathematical classification.")