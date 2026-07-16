# Phase 2, Day 38: The Forward Diffusion Process (Data Corruption)
import torch

print("--- Booting Diffusion Noise Scheduler ---")

# 1. Define the Timeline
# A standard diffusion model uses 1000 time steps. We will use 10 for diagnostics.
total_timesteps = 10

# 2. Define the Noise Schedule (Beta)
# Beta represents the percentage of noise added at each step.
# It starts incredibly small and gets larger over time.
beta_start = 0.0001
beta_end = 0.02
beta_schedule = torch.linspace(beta_start, beta_end, total_timesteps)

# Pre-calculate Alphas (1 - Beta), which represents how much original data remains
alpha_schedule = 1.0 - beta_schedule

# Cumulative product of Alphas (How much original data remains at step T relative to step 0)
alpha_cumprod = torch.cumprod(alpha_schedule, dim=0)

def forward_diffusion(x_0, t):
    """
    Instantly jumps to time step 't' and applies the exact mathematical amount 
    of Gaussian noise required for that specific step.
    """
    # Extract the scaling factors for the current time step
    sqrt_alpha_cumprod_t = torch.sqrt(alpha_cumprod[t])
    sqrt_one_minus_alpha_cumprod_t = torch.sqrt(1.0 - alpha_cumprod[t])
    
    # Generate pure Gaussian noise (The static)
    noise = torch.randn_like(x_0)
    
    # Mix the original image and the noise based on the schedule
    corrupted_data = (sqrt_alpha_cumprod_t * x_0) + (sqrt_one_minus_alpha_cumprod_t * noise)
    return corrupted_data, noise

# Simulating a clean, flat 1D "Image" (e.g., a perfect signal of 1.0s)
clean_data = torch.ones(1, 5)
print(f"Original Clean Data: {clean_data.tolist()[0]}\n")

# Simulate the timeline
print("Executing Systematic Forward Data Corruption...")
for step in range(total_timesteps):
    corrupted, applied_noise = forward_diffusion(clean_data, step)
    
    # We round the outputs just for clean terminal printing
    rounded = [round(val, 3) for val in corrupted.tolist()[0]]
    print(f"Time Step [T={step:02d}] | Remaining Signal: {alpha_cumprod[step].item():.3f} | Tensor: {rounded}")

print("\n--- Process Diagnostics ---")
print("Status: Forward diffusion scheduler operational. Data successfully decayed into Gaussian noise.")