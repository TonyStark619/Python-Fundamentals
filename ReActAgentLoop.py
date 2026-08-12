# Phase 3, Day 1: Autonomous ReAct (Reason + Act) Agent Loop
import re

print("--- Booting Autonomous ReAct Agent Loop ---")

# 1. The Tool Library (The Agent's Hands)
def calculate(expression):
    try:
        # A controlled sandbox evaluation
        return str(eval(expression, {"__builtins__": None}, {}))
    except Exception as e:
        return f"Error computing: {e}"

def search_database(query):
    # Simulating a vector DB or API lookup
    if "python" in query.lower():
        return "Python was released in 1991."
    return "No records found."

known_actions = {
    "Calculate": calculate,
    "Search": search_database
}

# 2. The Agent Logic Brain (Simulating the LLM Generator)
class ReActAgent:
    def __init__(self):
        self.system_prompt = """
        You run in a loop of Thought, Action, Observation.
        Use 'Action: ToolName[Input]' to use a tool.
        Available tools: Calculate, Search.
        When finished, output 'Final Answer: [Answer]'.
        """
        
    def mock_llm_generation(self, prompt_history):
        # In a real environment, you pass the prompt_history to an LLM here.
        # For simulation, we hardcode the autonomous steps the LLM would take.
        if "Observation:" not in prompt_history:
            return "Thought: I need to know when Python was released to calculate its age in 2026.\nAction: Search[Python release date]"
        elif "1991" in prompt_history and "Calculate" not in prompt_history:
            return "Thought: Python was released in 1991. The target year is 2026. I need to subtract.\nAction: Calculate[2026 - 1991]"
        else:
            return "Thought: The calculation returned 35.\nFinal Answer: Python will be 35 years old in 2026."

    def execute(self, user_objective, max_iterations=5):
        print(f"User Objective: {user_objective}\n")
        context = self.system_prompt + f"\nObjective: {user_objective}\n"
        
        action_regex = re.compile(r"Action: (\w+)\[(.*?)\]")
        
        for step in range(max_iterations):
            # 1. AI Generates a Thought and an Action
            ai_response = self.mock_llm_generation(context)
            print(f"--- Iteration {step + 1} ---")
            print(ai_response)
            
            context += ai_response + "\n"
            
            # 2. Check if the AI has solved the problem
            if "Final Answer:" in ai_response:
                print("\n[Engine] Objective achieved. Halting ReAct loop.")
                break
                
            # 3. Parse the Action and execute the Tool
            action_match = action_regex.search(ai_response)
            if action_match:
                action_name = action_match.group(1)
                action_input = action_match.group(2)
                
                if action_name in known_actions:
                    print(f"[System] Executing Tool: {action_name} with input: '{action_input}'")
                    observation = known_actions[action_name](action_input)
                else:
                    observation = f"Error: Tool {action_name} not found."
                
                print(f"Observation: {observation}\n")
                context += f"Observation: {observation}\n"

# Execute the Autonomous Environment
agent = ReActAgent()
agent.execute("How old will Python be in the year 2026?")

print("Status: Autonomous ReAct loop execution successful. Tool integration verified.")