# Phase 3, Day 11: Autonomous Agent Reflection & Self-Correction
print("--- Booting Agentic Reflection (System 2) Engine ---")

class SelfCorrectingAgent:
    def __init__(self):
        self.max_reflections = 2
        
    def mock_generate_initial_code(self, task):
        """Simulates the LLM's first, often flawed, attempt at solving the problem."""
        print("[Agent-Generator] Drafting initial solution...")
        return "def calculate_sum(a, b):\n    return a - b  # Oops, logic error"

    def mock_critique_code(self, code):
        """Simulates the LLM adopting a Critic persona to attack its own work."""
        print("[Agent-Critic] Analyzing draft for logical and syntax integrity...")
        if "a - b" in code:
            return "CRITIQUE: The task asks for a sum, but the code subtracts 'b' from 'a'. Operator should be '+'."
        return "CRITIQUE: Code appears mathematically sound."

    def mock_refine_code(self, code, critique):
        """Simulates the LLM rewriting the code based on the strict critique."""
        print("[Agent-Generator] Applying corrections based on critique...")
        if "Operator should be '+'" in critique:
            return "def calculate_sum(a, b):\n    return a + b"
        return code

    def execute_task(self, task):
        print(f"Objective: {task}\n")
        
        # Step 1: Zero-Shot Generation
        current_solution = self.mock_generate_initial_code(task)
        print(f"\n--- Initial Draft ---\n{current_solution}\n---------------------")
        
        # Step 2: The Reflection Loop
        for iteration in range(self.max_reflections):
            print(f"\nInitiating Reflection Loop {iteration + 1}...")
            
            critique = self.mock_critique_code(current_solution)
            print(f"Feedback: {critique}")
            
            # If the critic finds no flaws, we can confidently break the loop early
            if "mathematically sound" in critique:
                print("Validation passed. Early exit triggered.")
                break
                
            # If flawed, force the model to rewrite it
            current_solution = self.mock_refine_code(current_solution, critique)
            print(f"Refined Code:\n{current_solution}")
            
        return current_solution

# Execute the Autonomous Environment
agent = SelfCorrectingAgent()

final_output = agent.execute_task("Write a Python function to calculate the sum of two numbers.")

print("\n--- Final Validated Output ---")
print(final_output)
print("\nStatus: Reflection loop complete. Self-correction successful.")