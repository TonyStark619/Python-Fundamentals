# Phase 2, Day 23: Production-Grade CNN Regularization
import torch
import torch.nn as nn
import torch.nn.functional as F

print("--- Booting Regularized Vision Architecture ---")

class AdvancedVisionClassifier(nn.Module):
    def __init__(self):
        super().__init__()
        # 1. Feature Extraction Layer
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3)
        
        # Industry Standard: Batch Normalization for 2D spatial feature maps
        self.batch_norm = nn.BatchNorm2d(num_features=16)
        
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        
        # 2. Fully Connected Dense Brain (Flattened shape remains 16 * 13 * 13 = 2704)
        self.flat_features = 16 * 13 * 13 
        self.fc1 = nn.Linear(in_features=self.flat_features, out_features=64)
        
        # Industry Standard: Dropout layer. 
        # p=0.25 means a random 25% of connections are severed each step to prevent memorization
        self.dropout = nn.Dropout(p=0.25)
        
        self.fc2 = nn.Linear(in_features=64, out_features=10) # 10 final output classes

    def forward(self, x):
        # Apply convolution, instantly stabilize with batch norm, then activate and pool
        x = self.pool(F.relu(self.batch_norm(self.conv1(x))))
        
        # Flatten spatial maps to a 1D vector stream
        x = torch.flatten(x, start_dim=1)
        
        # Pass into first dense layer, activate, then apply dropout
        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        
        # Final classification inference
        x = self.fc2(x)
        return x

# Instantiate the optimized architecture
ai_model = AdvancedVisionClassifier()
print("\nRegularized Architecture Successfully Constructed:")
print(ai_model)

# Diagnostic verification with a mock grayscale image tensor
dummy_image = torch.randn(1, 1, 28, 28)
output = ai_model(dummy_image)

print("\n--- Model Execution Diagnostics ---")
print(f"Output Matrix Shape: {list(output.shape)} (Batch Size, Classes)")
print("Status: Regularization layers successfully integrated and stable.")