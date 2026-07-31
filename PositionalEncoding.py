# Phase 2, Day 53: Positional Encoding (Injecting Sequence Logic)
import torch
import torch.nn as nn
import math

print("--- Booting Positional Encoding Wave Generator ---")

class PositionalEncoding(nn.Module):
    def __init__(self, embed_dim, max_seq_length=5000):
        super().__init__()
        self.embed_dim = embed_dim
        
        # 1. Create a blank matrix to hold the positional waves (Sequence Length x Embedding Dimension)
        pe = torch.zeros(max_seq_length, embed_dim)
        
        # 2. Create a tensor representing the absolute position of each word (0, 1, 2, 3...)
        position = torch.arange(0, max_seq_length, dtype=torch.float).unsqueeze(1)
        
        # 3. Calculate the Frequency Divider
        # We use exponentiation and math.log to scale the frequencies down the embedding dimensions
        div_term = torch.exp(torch.arange(0, embed_dim, 2).float() * (-math.log(10000.0) / embed_dim))
        
        # 4. Inject Sine waves into the EVEN indexes (0, 2, 4...)
        pe[:, 0::2] = torch.sin(position * div_term)
        
        # 5. Inject Cosine waves into the ODD indexes (1, 3, 5...)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        # Add a batch dimension to match standard Transformer inputs: (1, seq_len, embed_dim)
        pe = pe.unsqueeze(0)
        
        # Register as a buffer: PyTorch will save this in the model state, 
        # but it knows NOT to update it during training (it's a fixed mathematical constant).
        self.register_buffer('pe', pe)

    def forward(self, x):
        # We slice the wave matrix to match the exact length of the incoming sentence
        seq_len = x.size(1)
        positional_wave = self.pe[:, :seq_len, :]
        
        # The Magic: We literally ADD the wave values to the original word embeddings
        x = x + positional_wave
        return x

# Initialize the architecture (Simulating a 256-dimension embedding)
encoder = PositionalEncoding(embed_dim=256)

# Simulating a sentence of 5 blank tokens
dummy_sentence = torch.zeros(1, 5, 256)

print("Injecting sine/cosine temporal waves into token embeddings...")
encoded_sentence = encoder(dummy_sentence)

print("\n--- Network Diagnostics ---")
print(f"Output Matrix Shape: {list(encoded_sentence.shape)}")

# Let's look at the first 4 dimensions of the first 3 words to see the waves acting
print("\nWave Traces (First 4 dimensions of first 3 words):")
for i in range(3):
    trace = [f"{val:.4f}" for val in encoded_sentence[0, i, :4].tolist()]
    print(f"Word {i+1} Vector Start: {trace}")

print("\nStatus: Temporal wave frequencies successfully injected. Transformer is now sequence-aware.")