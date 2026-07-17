# Phase 2, Day 39: U-Net Architecture (The Reverse Diffusion Engine)
import torch
import torch.nn as nn

print("--- Booting U-Net Denoising Architecture ---")

class SimpleUNet(nn.Module):
    def __init__(self):
        super().__init__()
        
        # 1. The Downsampling Encoder (Extracts deep mathematical context)
        # e.g., Shrinks a 1D sequence from 16 features down to 8
        self.encoder = nn.Sequential(
            nn.Linear(in_features=16, out_features=8),
            nn.ReLU()
        )
        
        # 2. The Bottleneck (The deepest layer of the network)
        self.bottleneck = nn.Sequential(
            nn.Linear(in_features=8, out_features=8),
            nn.ReLU()
        )
        
        # 3. The Upsampling Decoder (Rebuilds the data)
        # Notice it takes 16 inputs. This is because we concatenate (glue) the 8 bottleneck 
        # features with the 8 original high-res features from the skip connection.
        self.decoder = nn.Sequential(
            nn.Linear(in_features=16, out_features=16)
        )

    def forward(self, noisy_data):
        print(f"1. Ingesting Noisy Corrupted Data: {list(noisy_data.shape)}")
        
        # Phase A: Encode the data and SAVE it for the skip connection
        encoded_features = self.encoder(noisy_data)
        
        # Phase B: Process through the Bottleneck
        deep_features = self.bottleneck(encoded_features)
        print(f"2. Data Compressed at Bottleneck: {list(deep_features.shape)}")
        
        # Phase C: The Skip Connection (Concatenation)
        # We glue the bottleneck data and the saved encoder data side-by-side
        skip_connected_data = torch.cat((encoded_features, deep_features), dim=1)
        print(f"3. Skip Connection Bridged. Shape post-concat: {list(skip_connected_data.shape)}")
        
        # Phase D: Decode and Predict the Noise
        predicted_noise = self.decoder(skip_connected_data)
        return predicted_noise

# Initialize the architecture
denoiser = SimpleUNet()

# Simulating a noisy, corrupted 1D matrix from yesterday's Forward Diffusion
dummy_corrupted_data = torch.randn(1, 16)

print("\nExecuting Reverse Diffusion Pipeline...")
noise_prediction = denoiser(dummy_corrupted_data)

print("\n--- Network Diagnostics ---")
print(f"Output Matrix Shape (Predicted Noise): {list(noise_prediction.shape)}")
print("Status: U-Net Skip connections operational. Architecture is ready to subtract noise and restore reality.")