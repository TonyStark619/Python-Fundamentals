# Phase 3, Day 24: Deterministic Agent State Machine (Graph Architecture)
import time

print("--- Booting Agentic State Machine Engine ---")

class AgentStateEngine:
    def __init__(self):
        # We start at the initialization node
        self.state = "START"
        # The Context acts as the payload being passed between nodes
        self.context = {}

    def node_think(self):
        print("[Node: THINK] AI is analyzing the objective and selecting a tool...")
        self.context['action_required'] = True
        # Transitions to ACT
        return "ACT"

    def node_act(self):
        print("[Node: ACT] System executing local Python tool based on AI request...")
        self.context['tool_output'] = "{'status': 200, 'data': 'Target located.'}"
        # Transitions to OBSERVE
        return "OBSERVE"

    def node_observe(self):
        print(f"[Node: OBSERVE] AI evaluating tool payload: {self.context['tool_output']}")
        self.context['resolved'] = True
        
        # The Decision Edge: The LLM evaluates if the objective is complete
        if self.context.get('resolved'):
            print("[Decision Edge] Objective satisfied. Routing to END.")
            return "END"
        else:
            print("[Decision Edge] Objective incomplete. Looping back to THINK.")
            return "THINK"

    def execute(self):
        print("System Objective: Locate the target user profile.\n")
        
        # The Orchestrator Loop: Strictly bound by defined graph nodes
        while self.state != "END":
            print(f"--> Current State: {self.state}")
            
            if self.state == "START":
                self.state = "THINK"
            elif self.state == "THINK":
                self.state = self.node_think()
            elif self.state == "ACT":
                self.state = self.node_act()
            elif self.state == "OBSERVE":
                self.state = self.node_observe()
                
            time.sleep(0.5) # Simulating API latency
            
        print("--> Current State: END")
        print("\nStatus: State Machine graph traversal complete. Token hemorrhaging mathematically prevented.")

# Execution Environment
engine = AgentStateEngine()
engine.execute()