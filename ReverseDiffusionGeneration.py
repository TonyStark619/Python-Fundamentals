# Phase 2, Day 40: Reverse Diffusion (The Generative Loop)
import torch
import torch.nn as nn

print("--- Booting Generative Diffusion Loop ---")

# Simulating the U-Net from yesterday. 
# In production, this neural brain accurately predicts the noise pattern.
class DummyUNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.brain = nn.Linear(16, 16) # Mock architecture
        
    def forward(self, noisy_data, timestep):
        # The U-Net tries to predict the noise currently present in the data
        return torch.randn_like(noisy_data) * 0.1 # Simulating a small noise prediction

denoiser = DummyUNet()

# 1. Start with 100% Pure Static (Random Gaussian Noise)
# This represents a completely blank, chaotic canvas
synthetic_data = torch.randn(1, 16)
print(f"Initial State (Pure Static): {['{:.2f}'.format(x) for x in synthetic_data.tolist()[0][:5]]}...\n")

total_timesteps = 10

print("Initiating Reverse Diffusion Process...")

# 2. The Denoising Loop (Stepping backward from T=10 down to T=0)
for step in reversed(range(total_timesteps)):
    
    # Step A: The U-Net looks at the current static and predicts the noise pattern
    predicted_noise = denoiser(synthetic_data, step)
    
    # Step B: We mathematically subtract a fraction of that noise 
    # (In actual PyTorch implementations, this math involves the Alpha/Beta schedule from Day 68)
    # We will simulate the subtraction for architectural clarity:
    synthetic_data = synthetic_data - predicted_noise
    
    # Step C: Inject a tiny bit of new random noise back in (Langevin Dynamics) 
    # This prevents the AI from collapsing into blurry, average images.
    if step > 0:
        langevin_noise = torch.randn_like(synthetic_data) * 0.05
        synthetic_data = synthetic_data + langevin_noise

    # Print the stabilization of the data
    sample_preview = ['{:.2f}'.format(x) for x in synthetic_data.tolist()[0][:5]]
    print(f"Time Step [T={step:02d}] | Removing Static | Matrix State: {sample_preview}...")

print("\n--- Generation Complete ---")
print("Status: Synthetic data successfully sculpted from pure noise. Reverse Diffusion operational.")