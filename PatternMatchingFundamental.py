# Phase 3, Day 61: Python Fundamentals - Structural Pattern Matching
from dataclasses import dataclass

print("--- Booting Python Fundamental Data Parser ---")

# A standard data class simulating a database record
@dataclass
class EnterpriseUser:
    username: str
    access_level: int

def parse_incoming_payload(payload):
    """
    Utilizes match/case to execute complex structural unpacking of incoming API data.
    """
    print(f"\n[Parser] Analyzing incoming payload type: {type(payload).__name__}")
    
    match payload:
        
        # Pattern 1: Exact string match
        case "PING":
            return "200 OK: Service Active"
            
        # Pattern 2: List unpacking (Match exactly two elements, bind to variables)
        case ["LOG", error_msg]:
            return f"Writing to Logs: '{error_msg}'"
            
        # Pattern 3: Dictionary structural match (Matches the KEYS, extracts the VALUES)
        case {"status": 404, "route": missing_path}:
            return f"Alert: Client requested missing endpoint '{missing_path}'"
            
        # Pattern 4: Dictionary match with a Guard Clause ('if' statement inside the case)
        case {"action": "UPDATE", "user_id": uid, "data": new_data} if uid > 0:
            return f"Updating Database -> User {uid}: {new_data}"
            
        # Pattern 5: Custom Object unpacking
        case EnterpriseUser(username=name, access_level=level) if level >= 5:
            return f"CRITICAL: Admin '{name}' has authenticated."
            
        # Fallback Case (The Wildcard '_')
        case _:
            return "400 Bad Request: Invalid Payload Structure"

# --- Execution Environment ---
print("\n[System] Spawning API Payload Stream...")

payloads = [
    "PING",
    ["LOG", "Database timeout on Cluster 4"],
    {"status": 404, "route": "/api/v1/hidden"},
    {"action": "UPDATE", "user_id": 105, "data": {"theme": "dark"}},
    EnterpriseUser(username="Root_Admin", access_level=9),
    1024 # Invalid random integer
]

for item in payloads:
    result = parse_incoming_payload(item)
    print(f"  -> {result}")

print("\nStatus: Python fundamentals verified. Structural pattern unpacking resolved complex payloads without if/else logic.")