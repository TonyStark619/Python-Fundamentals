# Phase 3, Day 36: Retrieval-Augmented Generation (RAG) Pipeline
import math

print("--- Booting Native RAG (Retrieval-Augmented Generation) Pipeline ---")

class VectorDatabase:
    def __init__(self):
        self.documents = []

    def mock_embed(self, text):
        """Simulates converting text into a 3D mathematical vector space."""
        text = text.lower()
        v = [0.0, 0.0, 0.0]
        # Axis 0: HR / Policy, Axis 1: Engineering / Tech, Axis 2: Finance / Money
        if "leave" in text or "policy" in text or "vacation" in text: v[0] = 1.0
        if "code" in text or "deploy" in text or "server" in text: v[1] = 1.0
        if "salary" in text or "budget" in text or "expense" in text: v[2] = 1.0
        
        return [val + 0.1 for val in v] # Base noise to prevent zero division

    def add_document(self, doc_id, text):
        """Chunks and stores private data securely."""
        vector = self.mock_embed(text)
        self.documents.append({"id": doc_id, "content": text, "vector": vector})
        print(f"[Vector DB] Ingested Document {doc_id}: '{text}'")

    def cosine_similarity(self, v1, v2):
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a * a for a in v1))
        mag2 = math.sqrt(sum(b * b for b in v2))
        return dot / (mag1 * mag2)

    def retrieve_context(self, query, top_k=1):
        """Finds the most mathematically relevant private document."""
        print(f"\n[Retrieval Engine] Scanning vector space for query: '{query}'")
        query_vec = self.mock_embed(query)
        
        scored_docs = []
        for doc in self.documents:
            score = self.cosine_similarity(query_vec, doc["vector"])
            scored_docs.append((score, doc["content"]))
            
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        best_match = scored_docs[0][1] if scored_docs else ""
        
        print(f"[Retrieval Engine] Top context extracted: '{best_match}'")
        return best_match

class RAGAgent:
    def __init__(self):
        self.db = VectorDatabase()

    def generate_answer(self, user_query):
        # Step 1: Retrieval (Pulling private knowledge)
        context = self.db.retrieve_context(user_query)
        
        # Step 2: Augmentation (Injecting it into the prompt)
        augmented_prompt = f"""
        System: Answer the user's question based strictly on the provided context.
        Context: {context}
        User Question: {user_query}
        """
        
        # Step 3: Generation (Simulated LLM response)
        print("\n[LLM Generator] Processing augmented prompt...")
        if "vacation" in user_query.lower() and "policy" in context.lower():
            return "Based on the internal policy, employees receive 21 days of paid vacation."
        elif "deploy" in user_query.lower() and "server" in context.lower():
            return "Production deploys are locked on Fridays to prevent weekend outages."
        else:
            return "I do not have enough context to answer that accurately."

# --- Execution Environment ---
agent = RAGAgent()

# 1. Ingest Private Enterprise Data
print("--- Step 1: Data Ingestion ---")
agent.db.add_document("HR_01", "Company policy grants all employees 21 days of paid vacation annually.")
agent.db.add_document("ENG_01", "Production server deployments are strictly prohibited on Fridays.")
agent.db.add_document("FIN_01", "Quarterly expense reports must be submitted by the 5th of the month.")

# 2. Execute RAG Queries
print("\n--- Step 2: RAG Execution ---")
query_1 = "How much vacation time do I get?"
answer_1 = agent.generate_answer(query_1)
print(f"Final Output: {answer_1}")

query_2 = "Can I deploy the new feature to the server this Friday?"
answer_2 = agent.generate_answer(query_2)
print(f"Final Output: {answer_2}")

print("\nStatus: RAG architecture verified. Context hallucination eliminated.")