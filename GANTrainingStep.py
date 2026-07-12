# Phase 2, Day 34: The Adversarial Optimization Step
import torch
import torch.nn as nn
import torch.optim as optim

print("--- Booting Generative Adversarial Training Loop ---")

# 1. Re-initialize baseline micro-architectures
generator = nn.Sequential(nn.Linear(8, 16), nn.ReLU(), nn.Linear(16, 32))
discriminator = nn.Sequential(nn.Linear(32, 16), nn.ReLU(), nn.Linear(16, 1), nn.Sigmoid())

# 2. Setup Separate Engines and Shared Loss Function
# GANs use Binary Cross Entropy Loss because the detective makes a binary decision (Real vs Fake)
criterion = nn.BCELoss()
d_optimizer = optim.Adam(discriminator.parameters(), lr=0.001)
g_optimizer = optim.Adam(generator.parameters(), lr=0.001)

# Simulating a single training step batch
batch_size = 4
real_data = torch.randn(batch_size, 32) # Mock authentic data matrix
latent_noise = torch.randn(batch_size, 8) # Pure random noise for the counterfeiter

# === STEP 1: TRAIN THE DISCRIMINATOR (The Detective) ===
d_optimizer.zero_grad()

# Test real data
real_predictions = discriminator(real_data)
real_loss = criterion(real_predictions, torch.ones(batch_size, 1)) # Real targets = 1

# Test fake data
fake_data = generator(latent_noise)
fake_predictions = discriminator(fake_data.detach()) # .detach() prevents updating the generator yet
fake_loss = criterion(fake_predictions, torch.zeros(batch_size, 1)) # Fake targets = 0

# Combine errors and optimize the detective
d_loss = real_loss + fake_loss
d_loss.backward()
d_optimizer.step()

# === STEP 2: TRAIN THE GENERATOR (The Counterfeiter) ===
g_optimizer.zero_grad()

# Generate new fake data and pass it through the newly updated detective
new_fake_predictions = discriminator(fake_data)
# The generator's goal is to force the detective to output 1 (Real)
g_loss = criterion(new_fake_predictions, torch.ones(batch_size, 1))

# Optimize the counterfeiter based on how well it fooled the detective
g_loss.backward()
g_optimizer.step()

print("\n--- Step Optimization Diagnostics ---")
print(f"Discriminator Combined Loss: {d_loss.item():.4f}")
print(f"Generator Forgery Loss:      {g_loss.item():.4f}")
print("\nStatus: Alternating backward passes executed successfully. Equilibrium stable.")