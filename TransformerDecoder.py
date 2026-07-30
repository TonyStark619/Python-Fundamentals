# Phase 2, Day 52: Generative Transformer Decoder (Causal Masking)
import torch
import torch.nn as nn

print("--- Booting Generative Decoder Architecture ---")

class TransformerDecoderBlock(nn.Module):
    def __init__(self, embed_dim, num_heads, ff_hidden_dim, dropout=0.1):
        super().__init__()
        
        # 1. Masked Self-Attention (The Core Generative Engine)
        self.masked_attention = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, batch_first=True)
        self.norm1 = nn.LayerNorm(embed_dim)
        
        # 2. Feed-Forward Memorization Layer
        self.ffn = nn.Sequential(
            nn.Linear(embed_dim, ff_hidden_dim),
            nn.ReLU(),
            nn.Linear(ff_hidden_dim, embed_dim)
        )
        self.norm2 = nn.LayerNorm(embed_dim)
        self.dropout = nn.Dropout(dropout)

    # The Architectural Constraint: The Causal Mask
    def generate_square_subsequent_mask(self, size):
        # Creates a square matrix where everything above the diagonal is mathematically blocked
        # 0.0 means "allowed to look", -inf means "blinded"
        mask = torch.triu(torch.ones(size, size) * float('-inf'), diagonal=1)
        return mask

    def forward(self, x):
        seq_length = x.size(1)
        
        # Generate the strict blindfold for the current sequence length
        causal_mask = self.generate_square_subsequent_mask(seq_length)
        print(f"[Engine] Causal Mask generated for sequence length {seq_length}.")
        
        # Phase A: MASKED Self-Attention
        # We pass the blindfold directly into the attention mechanism
        attn_output, _ = self.masked_attention(x, x, x, attn_mask=causal_mask)
        
        # Residual Connection 1
        x = self.norm1(x + self.dropout(attn_output))
        
        # Phase B: Feed-Forward
        ffn_output = self.ffn(x)
        
        # Residual Connection 2
        x = self.norm2(x + self.dropout(ffn_output))
        
        return x, causal_mask

# Initialize the generative block (Simulating GPT specs: 256 embedding, 8 heads)
decoder_block = TransformerDecoderBlock(embed_dim=256, num_heads=8, ff_hidden_dim=1024)

# Simulating an embedded sentence sequence of 5 tokens being trained
dummy_sequence = torch.randn(1, 5, 256)

print("\nProcessing Sequence through Autoregressive Decoder...")
output_sequence, applied_mask = decoder_block(dummy_sequence)

print("\n--- Diagnostic Visualization (The Blindfold) ---")
print("Upper triangular matrix (-inf) prevents token [i] from seeing token [i+1]:")
print(applied_mask.numpy())

print("\n--- Network Diagnostics ---")
print(f"Output Matrix Shape: {list(output_sequence.shape)}")
print("Status: Causal masking active. Future-leaking prevented. Ready for autoregressive generation.")