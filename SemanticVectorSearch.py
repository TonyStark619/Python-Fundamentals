# Phase 2, Day 30: Vector Mathematics & Semantic Search
import torch
import torch.nn.functional as F

print("--- Booting Semantic Search Architecture ---")

# Simulating the mathematical vectors of three different sentences.
# In a real pipeline, an LLM Embedding model generates these automatically.

# Vector A: "How to prepare for Java DSA placements."
vector_a = torch.tensor([[0.8, 0.6, 0.1, 0.9]])

# Vector B: "Top interview questions for tech jobs." (High semantic overlap with A)
vector_b = torch.tensor([[0.7, 0.5, 0.2, 0.8]])

# Vector C: "Baking a chocolate cake without an oven." (Zero semantic overlap)
vector_c = torch.tensor([[-0.9, -0.8, 0.9, -0.2]])

print("Comparing Contextual Vectors using Cosine Similarity...\n")

# Calculate the angle (similarity) between Vector A and B
# An output close to 1.0 means identical meaning. Close to -1.0 means opposite.
similarity_a_b = F.cosine_similarity(vector_a, vector_b)

# Calculate the angle between Vector A and C
similarity_a_c = F.cosine_similarity(vector_a, vector_c)

print(f"Similarity Score [A vs B] (Tech vs Tech): {similarity_a_b.item():.4f}")
print(f"Similarity Score [A vs C] (Tech vs Baking): {similarity_a_c.item():.4f}")

print("\n--- Search Engine Output ---")
if similarity_a_b > similarity_a_c:
    print("AI correctly identified that Document B is the relevant match for Document A.")
else:
    print("Critical Failure in vector space.")
    
print("Status: Core RAG semantic retrieval engine operational.")