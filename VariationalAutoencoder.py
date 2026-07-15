# Phase 2, Day 37: Probabilistic Generative Engine (VAE)
import torch
import torch.nn as nn

print("--- Booting Variational Compression Architecture ---")

class VAE(nn.Module):
    def __init__(self):
        super().__init__()
        
        # 1. The Probabilistic Encoder
        self.fc1 = nn.Linear(in_features=784, out_features=400)
        # Instead of one latent vector, we output two: Mean (mu) and Variance (logvar)
        self.fc_mu = nn.Linear(in_features=400, out_features=20)      
        self.fc_logvar = nn.Linear(in_features=400, out_features=20)  
        
        # 2. The Generative Decoder
        self.fc3 = nn.Linear(in_features=20, out_features=400)
        self.fc4 = nn.Linear(in_features=400, out_features=784)

    def encode(self, x):
        h1 = torch.relu(self.fc1(x))
        return self.fc_mu(h1), self.fc_logvar(h1)

    # The Reparameterization Trick: Allows backpropagation to flow through randomness
    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar) # Convert log variance to standard deviation
        eps = torch.randn_like(std)   # Sample random noise
        return mu + eps * std         # Shift and scale the noise

    def decode(self, z):
        h3 = torch.relu(self.fc3(z))
        return torch.sigmoid(self.fc4(h3)) # Output bounded synthetic data

    def forward(self, x):
        # Step A: Compress into a mathematical probability cloud
        mu, logvar = self.encode(x)
        
        # Step B: Sample a specific point from that cloud
        z = self.reparameterize(mu, logvar)
        print(f"1. Data Compressed into Probability Distribution: {list(z.shape)}")
        
        # Step C: Reconstruct the synthetic data
        reconstructed = self.decode(z)
        print(f"2. Synthetic Data Sampled and Reconstructed: {list(reconstructed.shape)}")
        
        return reconstructed, mu, logvar

# Initialize the architecture
ai_model = VAE()

# Simulating high-dimensional raw data
raw_data_stream = torch.randn(1, 784)

print("\nExecuting Variational Compression Pipeline...")
out, mean, variance = ai_model(raw_data_stream)

print("\n--- Network Diagnostics ---")
print("Status: Reparameterization trick successful. Architecture is ready for generative sampling.")