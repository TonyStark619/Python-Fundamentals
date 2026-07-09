# Phase 2, Day 31: Retrieval-Augmented Generation (RAG)
import torch
import torch.nn.functional as F

print("--- Booting Enterprise RAG Pipeline ---")

# 1. The Secure Local Knowledge Base (Simulated as Vectors)
# In reality, this is a massive vector database like Pinecone or FAISS.
knowledge_base = {
    "Doc_1": {"text": "TCS Ninja requires strong array and string manipulation skills.", "vector": torch.tensor([[0.2, 0.8, 0.1]])},
    "Doc_2": {"text": "SAP Labs technical rounds focus heavily on dynamic programming and trees.", "vector": torch.tensor([[0.9, 0.3, 0.7]])},
    "Doc_3": {"text": "A standard pizza dough requires flour, water, yeast, and salt.", "vector": torch.tensor([[-0.5, -0.9, 0.1]])}
}

# 2. The User Query
user_query = "What data structures should I study for SAP?"
query_vector = torch.tensor([[0.8, 0.4, 0.8]]) # Simulated embedding of the user's question

print(f"User Query Received: '{user_query}'")
print("\nInitiating Phase 1: Semantic Vector Search...")

# 3. Retrieval Engine (Finding the facts)
best_match_id = None
highest_similarity = -1.0

for doc_id, data in knowledge_base.items():
    similarity = F.cosine_similarity(query_vector, data["vector"]).item()
    if similarity > highest_similarity:
        highest_similarity = similarity
        best_match_id = doc_id

retrieved_context = knowledge_base[best_match_id]["text"]
print(f"Retrieved Secure Context (Similarity: {highest_similarity:.2f}): '{retrieved_context}'")

# 4. Generation Engine (Injecting facts into the LLM prompt)
print("\nInitiating Phase 2: Augmented Generation...")

# We force the LLM to read the retrieved context before answering
augmented_prompt = f"Using ONLY the following context: '{retrieved_context}', answer the user's question: '{user_query}'"

# Simulating the LLM autoregressive output based strictly on the prompt
ai_response = "Based on the retrieved data, you should focus heavily on dynamic programming and trees for SAP Labs."

print("\n--- Final AI Output ---")
print(ai_response)
print("\nStatus: RAG Pipeline executed. Zero hallucination guarantee achieved.")