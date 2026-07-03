# Phase 2, Day 25: Foundations of Large Language Models (NLP)
import torch
import torch.nn as nn

print("--- Booting NLP Vector Space Architecture ---")

# 1. Defining the Dictionary (Vocabulary)
# Imagine our AI only knows 10 words total (Vocabulary Size = 10)
# We want to represent each word as a 4-dimensional mathematical vector
vocab_size = 10
embedding_dimensions = 4

# Initialize the Embedding Engine
word_embedder = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embedding_dimensions)
print(f"Status: Embedding space generated. {vocab_size} words mapped to {embedding_dimensions}D vectors.")

# 2. Simulating a Sentence Input
# Let's pretend our sentence is "AI is the future"
# These words correspond to their integer IDs in our dictionary: [2, 5, 1, 8]
sentence_indices = torch.tensor([2, 5, 1, 8])
print(f"\nRaw Input Sentence (Integer IDs): {sentence_indices.tolist()}")

# 3. Vector Translation
# We pass the integers through the embedder to get their true mathematical representation
dense_vectors = word_embedder(sentence_indices)

print("\n--- Output: Dense Vector Translation ---")
print(dense_vectors.detach().numpy())
print(f"\nFinal Matrix Shape: {list(dense_vectors.shape)} (Words, Dimensions)")
print("Status: Words successfully converted into trainable mathematical arrays.")