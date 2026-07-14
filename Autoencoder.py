# Phase 2, Day 36: Autoencoders (Bottleneck Architecture)
import torch
import torch.nn as nn

print("--- Booting Enterprise Autoencoder Architecture ---")

class DataCompressor(nn.Module):
    def __init__(self):
        super().__init__()
        
        # 1. The Encoder (Compresses massive data down to its core features)
        # e.g., Taking 784 data points and crushing them down to a 16-point footprint
        self.encoder = nn.Sequential(
            nn.Linear(in_features=784, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=16) # The Latent Bottleneck
        )
        
        # 2. The Decoder (Reconstructs the original data from the 16-point footprint)
        self.decoder = nn.Sequential(
            nn.Linear(in_features=16, out_features=128),
            nn.ReLU(),
            nn.Linear(in_features=128, out_features=784),
            nn.Sigmoid() # Keeps the output values scaled appropriately
        )

    def forward(self, x):
        # Step A: Compress the input
        latent_space = self.encoder(x)
        print(f"1. Data Compressed to Latent Space: {list(latent_space.shape)}")
        
        # Step B: Reconstruct the input
        reconstructed_data = self.decoder(latent_space)
        print(f"2. Data Reconstructed to Original Dimensions: {list(reconstructed_data.shape)}")
        
        return reconstructed_data

# Initialize the architecture
ai_model = DataCompressor()

# Simulating a high-dimensional input matrix (e.g., flattened image pixels or complex financial rows)
raw_data_stream = torch.randn(1, 784)

print("\nExecuting Compression and Reconstruction Pipeline...")
output_stream = ai_model(raw_data_stream)

print("\n--- Network Diagnostics ---")
print("Status: Bottleneck architecture operational. Ready for anomaly detection training loop.")