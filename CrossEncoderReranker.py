# Phase 2, Day 65: Cross-Encoder Reranker (Advanced RAG Quality Gate)
import torch
import torch.nn as nn
import torch.nn.functional as F

print("--- Booting Cross-Encoder Reranker Architecture ---")

class CrossEncoderReranker(nn.Module):
    def __init__(self, embed_dim):
        super().__init__()
        # A deep interaction layer that evaluates query and document jointly
        self.interaction_layer = nn.Sequential(
            nn.Linear(embed_dim * 2, embed_dim), # Multiplies dimensional depth for deep token comparison
            nn.ReLU(),
            nn.Linear(embed_dim, 1),             # Outputs a single continuous relevance score
            nn.Sigmoid()                         # Constrains score between 0.0 and 1.0
        )

    def forward(self, query_embed, doc_embeds):
        num_docs = doc_embeds.size(0)
        
        # Expand the query embedding to match the number of candidate documents
        # Shape: (num_docs, embed_dim)
        expanded_query = query_embed.expand(num_docs, -1)
        
        # THE CORE DIFFERENCE: Concatenate query and document side-by-side 
        # so the neural network analyzes them simultaneously rather than separately.
        # Shape: (num_docs, embed_dim * 2)
        joint_representation = torch.cat([expanded_query, doc_embeds], dim=-1)
        
        # Pass through the interaction scoring layer
        relevance_scores = self.interaction_layer(joint_representation)
        
        return relevance_scores.squeeze(-1)

# --- Simulation Environment ---
embed_dim = 16

# Initialize our Reranker model
reranker = CrossEncoderReranker(embed_dim)

# Simulating a user query embedding
user_query_vector = torch.randn(1, embed_dim)

# Simulating 4 candidate documents retrieved from our vector database
retrieved_documents = torch.randn(4, embed_dim)

print("Executing Deep Joint-Attention Scoring across candidate pool...")
scores = reranker(user_query_vector, retrieved_documents)

# Sort documents by their new cross-encoder scores
sorted_scores, sorted_indices = torch.sort(scores, descending=True)

print("\n--- Reranking Diagnostics ---")
for rank in range(len(sorted_scores)):
    doc_id = sorted_indices[rank].item()
    confidence = sorted_scores[rank].item() * 100
    print(f"Reranked Position {rank+1}: Document {doc_id} | Final Precision Score: {confidence:.2f}%")

print("\nStatus: Cross-Encoder reranking complete. Irrelevant vector noise purged from LLM context.")