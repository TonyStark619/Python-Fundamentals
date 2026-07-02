# Phase 2, Day 24: Enterprise Transfer Learning (ResNet-18)
import torch
import torch.nn as nn
import torchvision.models as models

print("--- Booting Transfer Learning Protocol ---")

# 1. Download the pre-trained ResNet-18 architecture (The Giant)
# This model already perfectly understands edges, shapes, lighting, and objects
ai_model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
print("Status: ResNet-18 baseline weights loaded into memory.")

# 2. Freeze the Core Brain (Prevent Autograd from destroying the pre-trained intelligence)
for param in ai_model.parameters():
    param.requires_grad = False
print("Status: Core architecture mathematically frozen.")

# 3. Architecture Modification (The Graft)
# ResNet-18 originally outputs to 1000 classes. We want to predict just 2 (e.g., Placed vs Not Placed)
# We find the exact number of input features going into its original final layer
in_features = ai_model.fc.in_features 

# We replace the final fully connected layer (fc) with our own custom, untrained layer
# Because this is a new layer, requires_grad is automatically True. 
# Only this single layer will update during training.
ai_model.fc = nn.Linear(in_features, 2)
print(f"Status: Final classification layer replaced. New output channels: 2.")

# Diagnostic verification with a mock RGB image tensor (Batch Size 1, 3 Channels, 224x224 Pixels)
dummy_image = torch.randn(1, 3, 224, 224)

print("\nExecuting Inference Pipeline through modified ResNet-18...")
output = ai_model(dummy_image)

print("\n--- Custom Model Output ---")
print(f"Output Matrix Shape: {list(output.shape)}")
print("Architecture is locked and ready for targeted training on custom datasets.")