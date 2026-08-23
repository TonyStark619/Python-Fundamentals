# Phase 3, Day 26: Human-in-the-Loop (HITL) Execution Guardrail
import time

print("--- Booting Human-in-the-Loop (HITL) Security Architecture ---")

# 1. The Tool Registry with Risk Metadata
class ToolRegistry:
    def __init__(self):
        self.tools = {
            "fetch_logs": {"func": self.fetch_logs, "risk": "LOW"},
            "drop_database_table": {"func": self.drop_database_table, "risk": "CRITICAL"}
        }

    def fetch_logs(self, target):
        return f"Returned 100 log lines for {target}."

    def drop_database_table(self, target):
        return f"CRITICAL: Table '{target}' has been permanently deleted."

# 2. The Orchestrator
class SecureAgentOrchestrator:
    def __init__(self):
        self.registry = ToolRegistry()

    def execute_tool_call(self, tool_name, arguments):
        print(f"\n[Agent] Requesting execution of: '{tool_name}'...")
        
        if tool_name not in self.registry.tools:
            return "Error: Unknown Tool."

        tool_meta = self.registry.tools[tool_name]
        
        # --- THE HITL INTERCEPTOR ---
        if tool_meta["risk"] == "CRITICAL":
            print(f"\n[SECURITY ALERT] Agent is attempting a CRITICAL action: {tool_name}({arguments})")
            print("[SECURITY ALERT] Execution paused. Awaiting Human Authorization.")
            
            # In a production web app, this triggers an API webhook or Slack message.
            # Here, we simulate the terminal block.
            human_override = input(">>> Approve execution? (y/N): ").strip().lower()
            
            if human_override != 'y':
                print("[System] Authorization DENIED. Agent operation blocked.")
                return "Action aborted by Human Supervisor."
            
            print("[System] Authorization GRANTED. Resuming execution...")

        # Execute the function
        result = tool_meta["func"](**arguments)
        print(f"[Execution Output] {result}")
        return result

# --- Simulation Environment ---
engine = SecureAgentOrchestrator()

print("\n--- Simulation 1: Low Risk Action ---")
# The AI decides to read some logs
engine.execute_tool_call("fetch_logs", {"target": "user_auth_service"})
time.sleep(1)

print("\n--- Simulation 2: Critical Risk Action ---")
# The AI hallucinates or decides it needs to wipe a table
engine.execute_tool_call("drop_database_table", {"target": "production_users"})

print("\nStatus: HITL checkpoint secured. Unsupervised destructive actions mathematically prevented.")