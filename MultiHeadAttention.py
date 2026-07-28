# Phase 2, Day 50: Multi-Head Attention (The Transformer Engine)
import torch
import torch.nn as nn
import torch.nn.functional as F
import math

print("--- Booting Multi-Head Attention Architecture ---")

class MHA(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        self.embed_dim = embed_dim
        self.num_heads = num_heads
        
        # Ensure the math perfectly divides
        assert embed_dim % num_heads == 0, "Embedding dimension must be divisible by number of heads"
        self.head_dim = embed_dim // num_heads
        
        # 1. The Projections (Linear Transformations for Query, Key, Value)
        self.q_proj = nn.Linear(embed_dim, embed_dim)
        self.k_proj = nn.Linear(embed_dim, embed_dim)
        self.v_proj = nn.Linear(embed_dim, embed_dim)
        
        # 2. The Output Consolidation Layer
        self.out_proj = nn.Linear(embed_dim, embed_dim)
        
    def forward(self, x):
        batch_size, seq_length, _ = x.size()
        
        # Step A: Project the data, then split into parallel 'Heads'
        # Shape transforms into: (batch_size, num_heads, seq_length, head_dim)
        Q = self.q_proj(x).view(batch_size, seq_length, self.num_heads, self.head_dim).transpose(1, 2)
        K = self.k_proj(x).view(batch_size, seq_length, self.num_heads, self.head_dim).transpose(1, 2)
        V = self.v_proj(x).view(batch_size, seq_length, self.num_heads, self.head_dim).transpose(1, 2)
        
        print(f"[Engine] Split data into {self.num_heads} parallel attention heads.")
        
        # Step B: Scaled Dot-Product Attention (Q * K^T) / sqrt(d_k)
        # This calculates how much focus every token should put on every other token
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.head_dim)
        
        # Step C: Convert raw scores into percentage weights (Softmax)
        attention_weights = F.softmax(scores, dim=-1)
        
        # Step D: Apply the weights to the actual Values
        attention_output = torch.matmul(attention_weights, V)
        
        # Step E: Recombine the Heads back into a single matrix
        attention_output = attention_output.transpose(1, 2).contiguous().view(batch_size, seq_length, self.embed_dim)
        print(f"[Engine] Concatenated head insights back to dimension {self.embed_dim}.")
        
        # Step F: Final Output Projection
        return self.out_proj(attention_output)

# Initialize the architecture (Simulating a mini-LLM with 256 dimensions and 8 heads)
model = MHA(embed_dim=256, num_heads=8)

# Simulating a sentence of 10 tokens (e.g., "How do I prepare for technical interviews at FAANG?")
dummy_sentence = torch.randn(1, 10, 256)

print("\nInitiating Parallel Semantic Analysis...")
final_context = model(dummy_sentence)

print("\n--- Process Diagnostics ---")
print(f"Input Matrix Shape:  {list(dummy_sentence.shape)}")
print(f"Output Matrix Shape: {list(final_context.shape)}")
print("Status: Parallel attention mechanisms operational. Semantic context successfully mapped.")