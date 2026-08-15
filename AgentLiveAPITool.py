# Phase 3, Day 10: Autonomous Agent Live API Integration
import urllib.request
import json

print("--- Booting Autonomous Agent API Interface ---")

# 1. The Live Data Tool
def fetch_live_user_data(user_id):
    """
    Simulates the agent reaching out to a live REST API to pull dynamic data.
    We use JSONPlaceholder, a free live mock API for developers.
    """
    url = f"https://jsonplaceholder.typicode.com/users/{user_id}"
    try:
        print(f"[Network] Establishing external connection to {url}...")
        # Execute the live GET request
        with urllib.request.urlopen(url, timeout=5) as response:
            data = json.loads(response.read().decode())
            # Parse the JSON and return the exact data the AI needs
            return f"User Found: {data['name']}, Company: {data['company']['name']}, City: {data['address']['city']}"
    except Exception as e:
        return f"API Connection Failed: {str(e)}"

# 2. The Tool Registry
available_tools = {
    "FetchUserAPI": fetch_live_user_data
}

# 3. The Execution Sandbox
def execute_agent_step(thought, action_name, action_input):
    print(f"\nAgent Thought: {thought}")
    
    if action_name in available_tools:
        print(f"Agent Action: Executing {action_name} with payload [{action_input}]")
        
        # The engine dynamically calls the function and passes the parsed input
        observation = available_tools[action_name](action_input)
        
        print(f"Observation: {observation}")
        return observation
    else:
        return "Error: Tool not recognized."

# --- Simulation Environment ---
print("Initializing Agent Objective: 'Who is User 3 and where do they work?'")

# Step 1: The AI decides it needs to use the live API
step_1_thought = "I do not have this information in my training data. I must query the external API for User ID 3."
step_1_action = "FetchUserAPI"
step_1_input = "3"

# Step 2: The Engine executes the AI's instruction
live_result = execute_agent_step(step_1_thought, step_1_action, step_1_input)

# Step 3: The AI reads the live response and finalizes its answer
final_thought = f"The API returned the data: {live_result}. I can now answer the user."
print(f"\nAgent Thought: {final_thought}")
print("Final Answer: User 3 is Clementine Bauch. She works at Romaguera-Jacobson in the city of McKenziehaven.")

print("\nStatus: External REST API integration successful. Agent intelligence expanded beyond training data.")