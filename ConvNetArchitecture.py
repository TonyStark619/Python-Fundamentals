# Phase 2, Day 21: Computer Vision & Convolutional Tensors
import torch
import torch.nn as nn

print("--- Booting PyTorch Vision Architecture ---")

class SimpleVisionBrain(nn.Module):
    def __init__(self):
        super().__init__()
        # Conv2d parameters: (input_channels, output_channels, kernel_size)
        # input_channels = 1 (Grayscale image). If it were RGB, it would be 3.
        # kernel_size = 3 (A 3x3 mathematical scanner passing over the image)
        self.convolution_layer = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=3)
        
        # MaxPool2d drastically reduces the image size to save memory, keeping only the brightest features
        self.pooling_layer = nn.MaxPool2d(kernel_size=2, stride=2)

    def forward(self, image_tensor):
        print(f"1. Raw Image Ingested: {list(image_tensor.shape)}")
        
        # Extract features (detecting edges and patterns)
        features = torch.relu(self.convolution_layer(image_tensor))
        print(f"2. Post-Convolution (Features Mapped): {list(features.shape)}")
        
        # Compress the data
        compressed = self.pooling_layer(features)
        print(f"3. Post-Pooling (Data Compressed): {list(compressed.shape)}")
        
        return compressed

# Initialize the Vision AI
vision_ai = SimpleVisionBrain()

# Simulating a batch of raw image data (Batch Size, Channels, Height, Width)
# e.g., 1 single Grayscale image that is 28x28 pixels
dummy_image_batch = torch.randn(1, 1, 28, 28)

print("\nExecuting Vision Inference Pipeline...")
output_tensor = vision_ai(dummy_image_batch)

print("\nStatus: Spatial feature extraction successful. Ready for classification layers.")