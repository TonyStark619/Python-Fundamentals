# Phase 2, Day 28: The Transformer Encoder Block (LLM Architecture)
import torch
import torch.nn as nn

print("--- Booting Transformer Encoder Architecture ---")

class TransformerEncoderBlock(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        
        # 1. The Attention Engine (From Yesterday)
        self.attention = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, batch_first=True)
        
        # 2. Normalization Layers (Keeps mathematical variance stable)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        
        # 3. The Feed Forward Brain (Expands the data, activates, then compresses it back)
        self.feed_forward = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.ReLU(),
            nn.Linear(embed_dim * 4, embed_dim)
        )

    def forward(self, x):
        print(f"1. Raw Sequence Ingested: {list(x.shape)}")
        
        # Step A: Attention Phase + Residual Connection (Add & Norm)
        attn_output, _ = self.attention(x, x, x)
        x = self.norm1(x + attn_output) # We add the original 'x' back in to prevent data loss
        print(f"2. Post-Attention Context Stabilized: {list(x.shape)}")
        
        # Step B: Feed Forward Phase + Residual Connection (Add & Norm)
        ff_output = self.feed_forward(x)
        x = self.norm2(x + ff_output)
        print(f"3. Post-Feed-Forward Output Generated: {list(x.shape)}")
        
        return x

# Initialize the full Transformer Block (Vectors: 16D, Heads: 4)
ai_block = TransformerEncoderBlock(embed_dim=16, num_heads=4)

# Simulating a sentence of 5 words
dummy_sequence = torch.randn(1, 5, 16)

print("\nExecuting Transformer Block Processing...")
final_output = ai_block(dummy_sequence)

print("\n--- Architecture Diagnostics ---")
print("Status: Add & Norm residual connections fully operational. Ready for stacking.")