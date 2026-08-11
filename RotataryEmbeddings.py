# Phase 2, Day 69: Rotary Position Embeddings (RoPE) - The Llama Standard
import torch
import math

print("--- Booting RoPE (Rotary Position Embedding) Architecture ---")

def apply_rotary_emb(x, seq_len, dim):
    """
    Applies mathematical rotation to the token embeddings.
    x shape: (Batch, Seq_Len, Dim)
    """
    # 1. Calculate the rotation frequencies (The Angles)
    # This dictates how fast the vectors will spin based on their depth in the embedding.
    position = torch.arange(seq_len, dtype=torch.float).unsqueeze(1)
    div_term = torch.exp(torch.arange(0, dim, 2).float() * -(math.log(10000.0) / dim))
    
    # 2. Generate the actual angles for every position
    freqs = position * div_term  # Shape: (Seq_Len, Dim/2)
    
    # 3. Duplicate frequencies so they apply to both halves of the embedding features
    # Shape becomes: (Seq_Len, Dim)
    emb = torch.cat((freqs, freqs), dim=-1)
    
    # 4. Generate the Cosine and Sine rotation matrices
    cos_matrix = torch.cos(emb).unsqueeze(0) # Add batch dimension
    sin_matrix = torch.sin(emb).unsqueeze(0)
    
    # 5. Execute the Rotation
    # We split the vector in half, flip the signs of the second half, and cross-multiply
    # Mathematically equivalent to: [x1*cos - x2*sin, x2*cos + x1*sin]
    x_half1 = x[..., :dim//2]
    x_half2 = x[..., dim//2:]
    x_rotated_half = torch.cat((-x_half2, x_half1), dim=-1)
    
    # The final mathematically rotated embedding
    x_out = (x * cos_matrix) + (x_rotated_half * sin_matrix)
    
    return x_out

# --- Simulation Environment ---
batch_size = 1
sequence_length = 4  # e.g., "Train LLMs from scratch"
embed_dim = 8

# Initialize a dummy query tensor (representing our token embeddings before attention)
q_tensor = torch.ones(batch_size, sequence_length, embed_dim)

print("Applying 2D Trigonometric Vector Rotation (RoPE)...")
q_rotated = apply_rotary_emb(q_tensor, sequence_length, embed_dim)

print("\n--- Diagnostic Visualization ---")
print("Original Vector (Word 1):")
print([round(val, 4) for val in q_tensor[0, 0, :].tolist()])

print("\nRotated Vector (Word 1 - Position 0):")
print([round(val, 4) for val in q_rotated[0, 0, :].tolist()])

print("\nRotated Vector (Word 2 - Position 1):")
print([round(val, 4) for val in q_rotated[0, 1, :].tolist()])

print("\nStatus: Tokens successfully rotated. Relative distance logic injected via Trigonometry.")