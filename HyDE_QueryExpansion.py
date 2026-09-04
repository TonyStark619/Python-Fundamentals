# Phase 3, Day 38: HyDE (Hypothetical Document Embeddings) Query Expansion
import math

print("--- Booting HyDE RAG Pipeline ---")

class HyDEVectorDatabase:
    def __init__(self):
        self.documents = []

    def _mock_embed(self, text):
        """Simulates mathematical semantic vectors."""
        text = text.lower()
        v = [0.0, 0.0]
        # Axis 0: Diagnostics/Errors, Axis 1: Code/Development
        if "timeout" in text or "error" in text or "latency" in text or "504" in text: v[0] = 1.0
        if "python" in text or "deploy" in text or "git" in text: v[1] = 1.0
        return [val + 0.1 for val in v]

    def add_document(self, doc_id, text):
        vector = self._mock_embed(text)
        self.documents.append({"id": doc_id, "content": text, "vector": vector})

    def cosine_similarity(self, v1, v2):
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a * a for a in v1))
        mag2 = math.sqrt(sum(b * b for b in v2))
        return dot / (mag1 * mag2)

    def retrieve(self, search_vector):
        """Retrieves based on the provided mathematical vector."""
        scored_docs = []
        for doc in self.documents:
            score = self.cosine_similarity(search_vector, doc["vector"])
            scored_docs.append((score, doc["content"]))
            
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return scored_docs[0][1]

class HyDEAgent:
    def __init__(self):
        self.db = HyDEVectorDatabase()

    def mock_llm_hallucinate_answer(self, vague_query):
        """
        Step 1: The LLM generates a HYPOTHETICAL answer to the vague query.
        This provides the semantic 'shape' and technical keywords needed for a good search.
        """
        print(f"\n[HyDE Expansion] LLM generating hypothetical document for query: '{vague_query}'")
        if "timeout" in vague_query:
            hypothetical_doc = "To fix a timeout, check the latency logs for error code 504. Increase the server response limit."
            print(f"  -> Generated Fake Answer: '{hypothetical_doc}'")
            return hypothetical_doc
        return vague_query

    def execute_hyde_search(self, raw_user_query):
        print(f"\n[System] Intercepted raw query: '{raw_user_query}'")
        
        # Step 1: Expand the query into a hypothetical document
        hypothetical_text = self.mock_llm_hallucinate_answer(raw_user_query)
        
        # Step 2: Embed the HYPOTHETICAL document, not the raw query
        print("[System] Embedding hypothetical document into vector space...")
        search_vector = self.db._mock_embed(hypothetical_text)
        
        # Step 3: Execute the search
        print("[Retrieval Engine] Searching database utilizing expanded vector...")
        best_match = self.db.retrieve(search_vector)
        
        return best_match

# --- Execution Environment ---
agent = HyDEAgent()

print("--- Data Ingestion ---")
agent.db.add_document("DOC_1", "Server Architecture: The Node.js instance requires 16GB of RAM.")
agent.db.add_document("DOC_2", "Troubleshooting: If a 504 Gateway Error occurs, the Nginx worker limit must be increased to resolve the timeout.")

# The user asks a terrible, vague question. A standard RAG would fail to match this.
bad_query = "fix the timeout"

# HyDE expands the bad query, generates fake context containing "latency" and "504", 
# and successfully maps to DOC_2.
retrieved_context = agent.execute_hyde_search(bad_query)

print(f"\n--- Final Retrieved Private Context ---")
print(retrieved_context)
print("\nStatus: HyDE expansion successful. Vague query resolved via hypothetical vector mapping.")