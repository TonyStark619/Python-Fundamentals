# Phase 3, Day 21: Pydantic Agent Guardrails
import json
from pydantic import BaseModel, Field, ValidationError

print("--- Booting Strict Pydantic Output Guardrails ---")

# 1. Define the Immutable AI Schema
# This forces the LLM's output to conform to strict data types and constraints.
class WeatherToolSchema(BaseModel):
    # Field enforces strict types and can add descriptions for the LLM
    location: str = Field(..., description="The city and country, e.g., 'Bhopal, India'")
    unit: str = Field(default="celsius", description="Temperature unit: 'celsius' or 'fahrenheit'")
    days_to_forecast: int = Field(..., ge=1, le=7, description="Number of days to forecast. Must be between 1 and 7.")

def execute_weather_tool(validated_data: WeatherToolSchema):
    """Executes only after the LLM payload has survived the Pydantic guardrail."""
    print(f"[System] Initiating meteorological scan for {validated_data.location}...")
    print(f"[System] Parameter check: {validated_data.days_to_forecast} day(s) in {validated_data.unit}.")
    return {"status": "success", "data": "Clear skies"}

def agent_router(raw_llm_json: str):
    print(f"\n[Agent Router] Intercepted raw LLM payload: {raw_llm_json}")
    
    try:
        # Step A: Standard JSON parse
        payload_dict = json.loads(raw_llm_json)
        
        # Step B: The Guardrail - Force the dictionary through the Pydantic schema
        print("[Guardrail] Validating payload against strict schema...")
        validated_payload = WeatherToolSchema(**payload_dict)
        
        print("[Guardrail] Validation PASSED. Payload is mathematically sound.")
        
        # Step C: Execution
        execute_weather_tool(validated_payload)
        
    except ValidationError as e:
        # Pydantic automatically catches data type errors and missing fields
        print("[Guardrail] CRITICAL BLOCK: LLM hallucinated invalid parameters.")
        for error in e.errors():
            print(f" -> Error in field '{error['loc'][0]}': {error['msg']}")
            
    except json.JSONDecodeError:
        print("[Guardrail] CRITICAL BLOCK: Payload is not valid JSON.")

# --- Simulation Environment ---

# Scenario 1: The AI perfectly follows instructions
perfect_llm_output = '{"location": "Bhopal, India", "unit": "celsius", "days_to_forecast": 3}'
agent_router(perfect_llm_output)

# Scenario 2: The AI hallucinates (Passes a string instead of an int, asks for 14 days when max is 7)
flawed_llm_output = '{"location": "Bangalore", "unit": "kelvin", "days_to_forecast": "fourteen"}'
agent_router(flawed_llm_output)

# Scenario 3: The AI forgets a required field entirely
missing_llm_output = '{"unit": "celsius"}'
agent_router(missing_llm_output)

print("\nStatus: Pydantic enforcement layer active. System integrity guaranteed against AI hallucinations.")