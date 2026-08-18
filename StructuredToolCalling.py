# Phase 3, Day 20: Native JSON Structured Tool Execution
import json

print("--- Booting Structured JSON Agent Interface ---")

# 1. The Local Software Environment (The Tools)
def get_weather(location, unit="celsius"):
    print(f"[System Execution] Accessing meteorological sensors for: {location}...")
    # Simulating a live API response
    return {"status": "success", "temperature": 28, "unit": unit, "forecast": "Clear skies"}

def execute_database_query(query_string):
    print(f"[System Execution] Querying main SQL cluster with: {query_string}...")
    return {"status": "success", "rows_returned": 1, "data": [{"username": "alex_tit", "role": "admin"}]}

# The function registry maps string names to actual memory addresses of Python functions
function_registry = {
    "get_weather": get_weather,
    "execute_database_query": execute_database_query
}

# 2. The Engine: Translating LLM JSON to Python Execution
def execute_llm_tool_call(llm_json_response):
    try:
        # Step A: Parse the raw text string from the LLM into a strict Python dictionary
        payload = json.loads(llm_json_response)
        
        function_name = payload.get("function")
        arguments = payload.get("arguments", {})
        
        print(f"\n[Agent Router] Intercepted structured request for: '{function_name}'")
        
        # Step B: Route the request to the local system
        if function_name in function_registry:
            target_function = function_registry[function_name]
            
            # **The Magic:** We use Python's ** unpacking to pass the JSON arguments directly into the function
            result = target_function(**arguments)
            
            print(f"[Agent Router] Execution successful. Result payload: {result}")
            return result
        else:
            print(f"[Agent Router] CRITICAL ERROR: LLM hallucinated an unregistered function: '{function_name}'")
            return None
            
    except json.JSONDecodeError:
        print("[Agent Router] CRITICAL ERROR: LLM failed to output valid JSON.")
        return None

# --- Simulation Environment ---
# Simulating the exact JSON string a modern LLM (like GPT-4) would generate
mock_llm_generation_1 = '{"function": "get_weather", "arguments": {"location": "Bhopal, India"}}'
mock_llm_generation_2 = '{"function": "execute_database_query", "arguments": {"query_string": "SELECT * FROM users WHERE id = 1"}}'

print("\nProcessing LLM Output Stream 1...")
execute_llm_tool_call(mock_llm_generation_1)

print("\nProcessing LLM Output Stream 2...")
execute_llm_tool_call(mock_llm_generation_2)

print("\nStatus: Native JSON tool calling architecture secured. Regex dependency eliminated.")