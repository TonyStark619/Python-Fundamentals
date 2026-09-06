# Phase 3, Day 41: Self-Reflective Agentic Loop (CRITIC Framework)
import time

print("--- Booting Self-Reflective CRITIC Architecture ---")

class ReflexionAgent:
    def __init__(self, max_retries=3):
        self.max_retries = max_retries

    def _mock_actor_generate(self, task, previous_feedback=None):
        """Simulates the LLM attempting to fulfill the prompt."""
        print("\n[Actor] Generating response payload...")
        time.sleep(1) # Simulating API latency
        
        # If the Actor receives negative feedback, it adjusts its next output
        if previous_feedback:
            print(f"  -> Applying Critic Feedback: '{previous_feedback}'")
            return "The production server is active. The IP address is 192.168.1.105."
            
        # First naive attempt (Hallucinates/misses the IP requirement)
        return "The production server is currently active and running smoothly."

    def _mock_critic_evaluate(self, response, original_task):
        """Simulates an LLM evaluating the response against the strict rules of the prompt."""
        print(f"[Critic] Analyzing generated response against original constraints...")
        
        # Hard constraint check: The user explicitly asked for the IP
        if "IP" in original_task and "192.168" not in response:
            feedback = "REJECTION: The user explicitly requested the IP address. You failed to provide it."
            print(f"  -> CRITIC VERDICT: FAILED. ({feedback})")
            return False, feedback
            
        print("  -> CRITIC VERDICT: PASSED. All constraints met.")
        return True, "SUCCESS"

    def execute_with_reflection(self, task):
        print(f"System Objective: '{task}'")
        
        current_feedback = None
        
        for attempt in range(1, self.max_retries + 1):
            print(f"\n--- Execution Loop {attempt}/{self.max_retries} ---")
            
            # Step 1: The Actor generates a draft
            draft_response = self._mock_actor_generate(task, current_feedback)
            print(f"[Draft Output]: '{draft_response}'")
            
            # Step 2: The Critic intercepts and evaluates
            is_valid, critique = self._mock_critic_evaluate(draft_response, task)
            
            if is_valid:
                print("\n[Orchestrator] Output validated. Releasing payload to user.")
                return draft_response
            else:
                print("[Orchestrator] Output blocked. Routing feedback back to Actor for regeneration.")
                current_feedback = critique
                
        return "CRITICAL FAILURE: Max reflection loops exceeded. Task aborted."

# --- Execution Environment ---
agent = ReflexionAgent()

# The user prompt contains a strict, specific requirement
complex_prompt = "Check the production server status and give me the exact IP address."

final_output = agent.execute_with_reflection(complex_prompt)

print("\n--- Final User-Facing Deliverable ---")
print(final_output)
print("\nStatus: Self-Reflective loop complete. Initial hallucination intercepted and autonomously corrected.")