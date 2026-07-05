# Phase 2, Day 27: Self-Attention (The Core of Transformers)
import torch
import torch.nn as nn

print("--- Booting Self-Attention Architecture ---")

class AttentionEngine(nn.Module):
    def __init__(self, embed_dim, num_heads):
        super().__init__()
        # MultiheadAttention allows the AI to focus on different parts of the sentence simultaneously
        # embed_dim: The size of our word vectors
        # num_heads: How many different "perspectives" the AI uses to look at the sentence
        self.attention = nn.MultiheadAttention(embed_dim=embed_dim, num_heads=num_heads, batch_first=True)

    def forward(self, sequence_tensor):
        print(f"1. Ingesting Sequence Matrix: {list(sequence_tensor.shape)}")
        
        # In Self-Attention, the Query, Key, and Value are all the exact same sequence
        # The AI is asking: "How does this sentence relate to itself?"
        attention_output, attention_weights = self.attention(
            query=sequence_tensor, 
            key=sequence_tensor, 
            value=sequence_tensor
        )
        
        print(f"2. Contextualized Output Generated: {list(attention_output.shape)}")
        return attention_output, attention_weights

# Initialize the architecture (Vectors: 16D, Heads: 4)
ai_model = AttentionEngine(embed_dim=16, num_heads=4)

# Simulating 1 batch, containing a 5-word sentence, where each word is a 16D vector
# [Batch Size, Sequence Length, Embedding Dimension]
dummy_sentence_vectors = torch.randn(1, 5, 16)

print("\nExecuting Simultaneous Attention Processing...")
context_vectors, weight_matrix = ai_model(dummy_sentence_vectors)

print("\n--- Model Output ---")
print(f"Attention Weights Shape: {list(weight_matrix.shape)} (Words mapping to other words)")
print("Status: Contextual relationships successfully mathematically mapped.")