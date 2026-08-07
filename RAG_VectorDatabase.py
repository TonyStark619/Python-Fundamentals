# Phase 2, Day 60: RAG Vector Search Engine (Cosine Similarity)
import torch
import torch.nn.functional as F

print("--- Booting RAG Vector Search Architecture ---")

def retrieve_top_k_documents(query_embedding, document_database, k=2):
    # 1. Normalize the vectors
    # Cosine similarity requires vectors to have a length (magnitude) of exactly 1.
    # This ensures we measure the DIRECTION of the data, ignoring how long the text is.
    query_norm = F.normalize(query_embedding, p=2, dim=1)
    doc_norm = F.normalize(document_database, p=2, dim=1)
    
    # 2. Compute Cosine Similarity
    # By taking the mathematical dot product of normalized vectors, 
    # we get a score from -1.0 (completely opposite) to 1.0 (perfectly identical).
    # Shape: (1, embed_dim) * (num_docs, embed_dim)^T -> (1, num_docs)
    similarity_scores = torch.matmul(query_norm, doc_norm.transpose(0, 1)).squeeze(0)
    
    # 3. Retrieve the Top-K highest matching documents
    top_k_scores, top_k_indices = torch.topk(similarity_scores, k=k)
    
    return top_k_scores, top_k_indices

# --- Simulation Environment ---
# Imagine an embedding dimension of 4 (usually 768 or 1536 in production)
embed_dim = 4

# Simulating 5 documents already processed and stored in our Vector Database
print("Loading Enterprise Vector Database (5 Documents)...")
vector_db = torch.tensor([
    [0.1, 0.2, 0.8, -0.1], # Doc 0: About Python
    [0.9, -0.2, 0.1, 0.0], # Doc 1: About Java
    [0.2, 0.3, 0.7, -0.2], # Doc 2: About Machine Learning (Similar to Python)
    [-0.5, 0.8, 0.1, 0.4], # Doc 3: About Web Dev
    [0.8, -0.1, 0.2, 0.1]  # Doc 4: About C++ (Similar to Java)
])

# Simulating the user asking: "Tell me about Python data science."
user_query = torch.tensor([[0.1, 0.3, 0.9, -0.2]])

print("Executing Cosine Similarity Vector Scan...")
# We want the top 2 most relevant documents to inject into our LLM prompt
scores, indices = retrieve_top_k_documents(user_query, vector_db, k=2)

print("\n--- RAG Retrieval Diagnostics ---")
for rank in range(len(scores)):
    doc_id = indices[rank].item()
    confidence = scores[rank].item() * 100
    print(f"Rank {rank+1}: Retrieved Document {doc_id} | Similarity Confidence: {confidence:.2f}%")

print("\nStatus: Semantic vector search complete. Context is ready for LLM prompt injection.")