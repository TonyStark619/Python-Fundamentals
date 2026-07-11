# Phase 2, Day 33: Generative Adversarial Networks (The Duel)
import torch
import torch.nn as nn

print("--- Booting Adversarial AI Architecture ---")

# 1. The Generator (The Counterfeiter)
# Goal: Take random mathematical noise and forge it into structured data
class Generator(nn.Module):
    def __init__(self):
        super().__init__()
        self.brain = nn.Sequential(
            nn.Linear(in_features=16, out_features=32),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=64) # Outputs a "fake" 64-point data matrix
        )

    def forward(self, noise):
        return self.brain(noise)

# 2. The Discriminator (The Detective)
# Goal: Inspect data and mathematically determine if it is REAL (1) or FAKE (0)
class Discriminator(nn.Module):
    def __init__(self):
        super().__init__()
        self.brain = nn.Sequential(
            nn.Linear(in_features=64, out_features=32),
            nn.ReLU(),
            nn.Linear(in_features=32, out_features=1),
            nn.Sigmoid() # Squashes the final confidence score strictly between 0 and 1
        )

    def forward(self, data):
        return self.brain(data)

# Initialize the competing architectures
counterfeiter = Generator()
detective = Discriminator()

# Step A: The Counterfeiter generates fake data from pure random noise
random_noise = torch.randn(1, 16)
forged_data = counterfeiter(random_noise)
print(f"1. Generator forged a synthetic matrix: {list(forged_data.shape)}")

# Step B: The Detective inspects the forged data
# (We use .detach() to ensure the Generator's math isn't accidentally updated during the Detective's turn)
detection_score = detective(forged_data.detach())

print("\n--- Network Diagnostics ---")
print(f"Discriminator Confidence (1.0 = Real, 0.0 = Fake): {detection_score.item():.4f}")
print("Status: Adversarial loop initialized. Networks are ready to continuously optimize against each other.")