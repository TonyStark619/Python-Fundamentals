# Day 15: JSON Handling - The language of AI APIs
import json

# Simulating an API response from a cloud AI service (Notice it's a string)
api_response = '{"model": "VisionPro_v2", "status": "active", "latency_ms": 42}'

# Parsing the JSON string into a Python Dictionary
parsed_data = json.loads(api_response)

print(f"Connected to Model: {parsed_data['model']}")
print(f"Current Status: {parsed_data['status'].upper()}")
print(f"Ping: {parsed_data['latency_ms']} ms")