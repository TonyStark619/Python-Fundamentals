# Phase 3, Day 22: Semantic Vector Memory Engine
import math

print("--- Booting Semantic Long-Term Agent Memory ---")

class SemanticMemoryBuffer:
    def __init__(self):
        self.memory_vault = []
    
    # 1. The Mock Embedding Engine
    def _mock_text_to_vector(self, text):
        """
        In production, this calls an Embedding Model (like text-embedding-3-small).
        For simulation, we map keywords to a simple 3D mathematical space.
        """
        text = text.lower()
        v = [0.0, 0.0, 0.0]
        if "password" in text or "secret" in text: v[0] = 1.0  # Security axis
        if "database" in text or "sql" in text:    v[1] = 1.0  # Tech axis
        if "project" in text or "deadline" in text:v[2] = 1.0  # Planning axis
        
        # Add slight base noise to prevent zero-vectors
        return [val + 0.1 for val in v]

    # 2. The Storage Mechanism
    def store_memory(self, content):
        vector = self._mock_text_to_vector(content)
        self.memory_vault.append({
            "content": content,
            "vector": vector
        })
        print(f"[Memory Vault] Stored: '{content}'")

    # 3. The Retrieval Engine (Cosine Similarity)
    def _cosine_similarity(self, vec_a, vec_b):
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        magnitude_a = math.sqrt(sum(a * a for a in vec_a))
        magnitude_b = math.sqrt(sum(b * b for b in vec_b))
        return dot_product / (magnitude_a * magnitude_b)

    def retrieve_relevant_context(self, current_query, top_k=2):
        print(f"\n[Search Engine] Querying vault for contextual matches to: '{current_query}'...")
        query_vector = self._mock_text_to_vector(current_query)
        
        # Score every memory in the vault against the current query
        scored_memories = []
        for mem in self.memory_vault:
            score = self._cosine_similarity(query_vector, mem["vector"])
            scored_memories.append((score, mem["content"]))
            
        # Sort by highest similarity
        scored_memories.sort(key=lambda x: x[0], reverse=True)
        
        # Extract the absolute most relevant past interactions
        retrieved = [mem[1] for mem in scored_memories[:top_k]]
        return retrieved

# --- Execution Environment ---
agent_memory = SemanticMemoryBuffer()

# Simulating a long conversation over several days
print("\n--- Ingesting Past Interactions ---")
agent_memory.store_memory("My project deadline is Friday.")
agent_memory.store_memory("I like eating pizza.")
agent_memory.store_memory("The production database SQL password is 'SecureRoot123'.")
agent_memory.store_memory("It is raining in Bhopal today.")

# A new query comes in. A sliding window would have deleted the password by now.
new_user_query = "What is the password for the database again?"

# The AI dynamically pulls only what matters
relevant_context = agent_memory.retrieve_relevant_context(new_user_query)

print("\n--- AI Context Injection ---")
for idx, ctx in enumerate(relevant_context):
    print(f"Context [{idx+1}]: {ctx}")

print("\nStatus: Semantic retrieval successful. Infinite context window achieved without token overflow.")