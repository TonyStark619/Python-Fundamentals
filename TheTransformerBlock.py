# Phase 2, Day 51: The Core Transformer Encoder Block
import torch
import torch.nn as nn

print("--- Booting Transformer Encoder Architecture ---")

class TransformerEncoderBlock(nn.Module):
    def __init__(self, embed_dim, num_heads, ff_hidden_dim, dropout=0.1):
        super().__init__()
        
        # 1. The Core Attention Engine (Using PyTorch's highly optimized built-in module)
        self.attention = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, batch_first=True)
        
        # 2. Feed-Forward Network (The Memorization Engine)
        # It expands the dimension to learn complex features, then shrinks it back down
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, ff_hidden_dim),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(ff_hidden_dim, embed_dim)
        )
        
        # 3. Layer Normalization (The Stabilizers)
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)
        
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # Phase A: Self-Attention with Residual Connection
        # We save a copy of 'x' (the original input)
        attention_output, _ = self.attention(x, x, x)
        
        # The Skip Connection: We add 'x' directly to the attention output
        x = self.norm1(x + self.dropout(attention_output))
        print("[Engine] Phase A Complete: Self-Attention insights merged with original data via Skip Connection.")
        
        # Phase B: Feed-Forward with Residual Connection
        ffn_output = self.ffn(x)
        
        # The Second Skip Connection
        x = self.norm2(x + self.dropout(ffn_output))
        print("[Engine] Phase B Complete: Feed-Forward patterns extracted and normalized.")
        
        return x

# Initialize the architecture 
# (Simulating standard BERT/GPT micro-block specs: 256 embedding, 8 heads, 1024 feed-forward expansion)
transformer_block = TransformerEncoderBlock(embed_dim=256, num_heads=8, ff_hidden_dim=1024)

# Simulating an embedded sentence sequence (Batch Size: 1, Tokens: 10, Embedding: 256)
dummy_sequence = torch.randn(1, 10, 256)

print("\nProcessing Sequence through Transformer Block...")
final_encoded_sequence = transformer_block(dummy_sequence)

print("\n--- Network Diagnostics ---")
print(f"Input Matrix Shape:  {list(dummy_sequence.shape)}")
print(f"Output Matrix Shape: {list(final_encoded_sequence.shape)}")
print("Status: Residual connections stable. Transformer block is ready for stacking.")