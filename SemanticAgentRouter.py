# Phase 3, Day 28: Semantic Vector-Based Agent Routing
import math

print("--- Booting Semantic Agent Routing Layer ---")

class SemanticRouter:
    def __init__(self):
        # The Routes: We define what each sub-agent is responsible for
        self.routes = {
            "sql_agent": "Queries the database, extracts user data, tabular information, rows, SQL.",
            "weather_agent": "Fetches meteorological data, temperature, climate, weather conditions.",
            "chit_chat_agent": "General conversation, greetings, jokes, small talk, harmless chat."
        }
        self.route_embeddings = {name: self._mock_embed(desc) for name, desc in self.routes.items()}

    # 1. The Mock Embedding Engine (Simulating a fast local embedding model)
    def _mock_embed(self, text):
        text = text.lower()
        # [DB Axis, Weather Axis, Chat Axis]
        v = [0.0, 0.0, 0.0]
        if any(w in text for w in ["database", "sql", "user", "data"]): v[0] = 1.0
        if any(w in text for w in ["weather", "temperature", "climate"]): v[1] = 1.0
        if any(w in text for w in ["hello", "joke", "chat", "hi"]): v[2] = 1.0
        
        # Add baseline noise
        return [val + 0.1 for val in v]

    # 2. Fast Cosine Similarity
    def _cosine_similarity(self, vec_a, vec_b):
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        mag_a = math.sqrt(sum(a * a for a in vec_a))
        mag_b = math.sqrt(sum(b * b for b in vec_b))
        return dot_product / (mag_a * mag_b)

    # 3. The Router Execution
    def route_query(self, user_query):
        print(f"\n[Router] Intercepted Request: '{user_query}'")
        
        # Instantly vectorize the user's prompt
        query_vector = self._mock_embed(user_query)
        
        best_match = None
        highest_score = -1.0
        
        # Compare against all pre-calculated route vectors
        for route_name, route_vec in self.route_embeddings.items():
            score = self._cosine_similarity(query_vector, route_vec)
            print(f"  -> {route_name} confidence: {score * 100:.1f}%")
            
            if score > highest_score:
                highest_score = score
                best_match = route_name
                
        # Fallback to general chat if confidence is too low
        if highest_score < 0.5:
            best_match = "chit_chat_agent"
            
        print(f"[Router Action] Fast-routing payload to >>> {best_match.upper()} <<< (Zero LLM tokens burned)")
        return best_match

# --- Execution Environment ---
router = SemanticRouter()

# The system instantly routes queries based on mathematical vectors, bypassing LLM reasoning latency
router.route_query("Find all users in the production database who logged in today.")
router.route_query("What's the temperature going to be in Bhopal tomorrow?")
router.route_query("Hey there, how are you doing today?")

print("\nStatus: Semantic routing active. Deterministic payload distribution achieved at minimal latency.")