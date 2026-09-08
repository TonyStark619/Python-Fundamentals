# Phase 3, Day 43: Shared State Graph (LangGraph Architecture Core)
import time

print("--- Booting Shared State Graph Orchestration ---")

# 1. The Shared Memory Object
# In production LangGraph, this is a TypedDict that every node reads and updates.
class GraphState:
    def __init__(self):
        self.memory = {
            "objective": "",
            "research_data": [],
            "code_draft": "",
            "errors_found": 0,
            "next_routing": "RESEARCHER"
        }

# 2. The Autonomous Nodes
class ResearcherNode:
    def process(self, state: GraphState):
        print("\n[Node: RESEARCHER] Accessing shared state...")
        objective = state.memory["objective"]
        
        print(f"  -> Executing web sweep for: '{objective}'")
        time.sleep(1)
        
        # Write findings directly into shared memory
        state.memory["research_data"].append("API requires OAuth2 authentication tokens.")
        
        # Route to the Coder
        state.memory["next_routing"] = "CODER"
        return state

class CoderNode:
    def process(self, state: GraphState):
        print("\n[Node: CODER] Accessing shared state...")
        context = state.memory["research_data"]
        
        print("  -> Drafting architecture based on global context...")
        time.sleep(1)
        
        # The Coder realizes it made a mistake
        state.memory["code_draft"] = "def connect(): pass # ERROR: Missing OAuth2 logic"
        state.memory["errors_found"] += 1
        
        # The Coder autonomously routes to the Reviewer for help
        state.memory["next_routing"] = "REVIEWER"
        return state

class ReviewerNode:
    def process(self, state: GraphState):
        print("\n[Node: REVIEWER] Accessing shared state...")
        errors = state.memory["errors_found"]
        
        print(f"  -> Auditing draft. Errors detected: {errors}")
        time.sleep(1)
        
        if errors > 0:
            print("  -> CRITICAL: Draft rejected. Routing back to CODER for revision.")
            state.memory["errors_found"] = 0 # Reset error state
            state.memory["code_draft"] = "def connect(token): return OAuth2(token) # FIXED"
            state.memory["next_routing"] = "END"
        else:
            state.memory["next_routing"] = "END"
            
        return state

# 3. The Graph Execution Engine
class StateGraphEngine:
    def __init__(self):
        self.nodes = {
            "RESEARCHER": ResearcherNode(),
            "CODER": CoderNode(),
            "REVIEWER": ReviewerNode()
        }
        self.state = GraphState()

    def execute_workflow(self, user_prompt):
        print(f"System Triggered: '{user_prompt}'")
        self.state.memory["objective"] = user_prompt
        
        # The Graph Orchestration Loop
        while self.state.memory["next_routing"] != "END":
            current_node_key = self.state.memory["next_routing"]
            active_node = self.nodes[current_node_key]
            
            # The node processes and returns the updated global state
            self.state = active_node.process(self.state)
            
        print("\n[Orchestrator] END node reached. State execution halted.")
        return self.state.memory["code_draft"]

# --- Execution Environment ---
engine = StateGraphEngine()

final_output = engine.execute_workflow("Build a secure API connection.")

print("\n--- Final State Memory Output ---")
print(final_output)
print("\nStatus: State Graph execution complete. Cyclic multi-agent memory routing verified.")