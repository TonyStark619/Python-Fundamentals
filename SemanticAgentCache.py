# Phase 3, Day 40: Semantic Output Caching (Token Optimization)
import math
import time

print("--- Booting Agentic Semantic Cache Layer ---")

class SemanticCache:
    def __init__(self, threshold=0.92):
        self.cache_vault = []
        self.similarity_threshold = threshold

    def _mock_embed(self, text):
        """Simulates rapid local embedding of a user prompt."""
        text = text.lower()
        v = [0.0, 0.0]
        # Axis 0: Authentication / Passwords, Axis 1: Billing / Money
        if "password" in text or "reset" in text or "login" in text: v[0] = 1.0
        if "billing" in text or "invoice" in text or "pay" in text: v[1] = 1.0
        return [val + 0.1 for val in v] # Base noise

    def _cosine_similarity(self, v1, v2):
        dot = sum(a * b for a, b in zip(v1, v2))
        mag1 = math.sqrt(sum(a * a for a in v1))
        mag2 = math.sqrt(sum(b * b for b in v2))
        return dot / (mag1 * mag2)

    def check_cache(self, user_query):
        """Scans the cache for semantically identical past queries."""
        query_vec = self._mock_embed(user_query)
        
        for entry in self.cache_vault:
            score = self._cosine_similarity(query_vec, entry["vector"])
            if score >= self.similarity_threshold:
                print(f"[Cache HIT] Semantic match found ({score * 100:.1f}% similarity).")
                return entry["response"]
                
        print("[Cache MISS] No semantic match found. Query must be routed to LLM.")
        return None

    def store_cache(self, query, llm_response):
        """Saves a new LLM response into the vector cache."""
        vector = self._mock_embed(query)
        self.cache_vault.append({
            "query": query, 
            "vector": vector, 
            "response": llm_response
        })
        print(f"[Cache WRITE] Stored new response payload for future rapid retrieval.")

class CostOptimizedAgent:
    def __init__(self):
        self.cache = SemanticCache()

    def handle_request(self, user_query):
        print(f"\n[System] Intercepted Request: '{user_query}'")
        
        # Step 1: The Cache Check (Cost: 0 tokens, 10ms latency)
        cached_answer = self.cache.check_cache(user_query)
        if cached_answer:
            return f"FAST RETURN: {cached_answer}"
            
        # Step 2: The LLM API Call (Cost: $$$ tokens, 3000ms latency)
        print("[LLM Routing] Executing expensive external API call to AI Model...")
        time.sleep(1.5) # Simulating API network latency
        
        llm_answer = ""
        if "password" in user_query.lower():
            llm_answer = "To reset your password, navigate to Settings > Security > Reset."
        else:
            llm_answer = "Please check our documentation for more details."
            
        # Step 3: Write the expensive answer to the cache
        self.cache.store_cache(user_query, llm_answer)
        
        return f"LLM GENERATED: {llm_answer}"

# --- Execution Environment ---
agent = CostOptimizedAgent()

# User 1 asks about a password. The system takes the hit and queries the LLM.
print("--- User 1 Execution ---")
response_1 = agent.handle_request("How do I reset my password?")
print(response_1)

# User 2 asks the EXACT same semantic question, but phrased differently.
# The cache intercepts it mathematically. The LLM is never triggered.
print("\n--- User 2 Execution ---")
response_2 = agent.handle_request("I forgot my password, how can I change it?")
print(response_2)

print("\nStatus: Semantic cache architecture verified. Redundant token generation mathematically blocked.")