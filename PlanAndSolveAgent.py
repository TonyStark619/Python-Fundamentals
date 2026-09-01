# Phase 3, Day 35: Plan-and-Solve Agent Architecture
import json

print("--- Booting Plan-and-Solve Agent Architecture ---")

class PlanAndSolveAgent:
    def __init__(self):
        self.execution_state = {}

    def mock_planner(self, objective):
        """
        Simulates the Planner LLM breaking a high-level prompt into an 
        explicit sequential execution plan.
        """
        print(f"\n[Planner] Analyzing high-level objective: '{objective}'")
        # The Planner outputs an ordered list of atomic tasks
        plan = [
            {"step_id": 1, "task": "Fetch system performance metrics", "tool": "metrics_collector"},
            {"step_id": 2, "task": "Identify CPU bottleneck threshold", "tool": "anomaly_detector"},
            {"step_id": 3, "task": "Generate mitigation recommendation", "tool": "report_generator"}
        ]
        print(f"[Planner] Generated {len(plan)}-step structured execution plan.")
        return plan

    def mock_tool_execution(self, tool_name, task_context):
        """Simulates tool execution for an individual step."""
        print(f"  -> Executing Tool [{tool_name}] for: '{task_context}'")
        if tool_name == "metrics_collector":
            return {"cpu_load": "94%", "memory_load": "61%", "io_wait": "12ms"}
        elif tool_name == "anomaly_detector":
            return {"bottleneck": "CPU core 0 saturated", "severity": "HIGH"}
        elif tool_name == "report_generator":
            return "Recommendation: Autoscale cluster and offload background workers to worker queue."
        return "Unknown task"

    def execute_objective(self, high_level_goal):
        print(f"System Goal: {high_level_goal}")

        # Step 1: Planning Phase
        execution_plan = self.mock_planner(high_level_goal)

        # Step 2: Execution Loop
        print("\n[Executor] Initiating sequential plan execution...")
        for step in execution_plan:
            step_id = step["step_id"]
            task = step["task"]
            tool = step["tool"]

            print(f"\n--- Step {step_id}: {task} ---")
            
            # Execute step and save result into centralized state memory
            step_result = self.mock_tool_execution(tool, task)
            self.execution_state[f"step_{step_id}_output"] = step_result
            print(f"  [Result Logged]: {step_result}")

        # Step 3: Synthesis Phase
        print("\n[Synthesizer] Compiling final response from plan outputs...")
        final_summary = self.execution_state.get("step_3_output", "Execution failed")
        return final_summary

# --- Execution Environment ---
agent = PlanAndSolveAgent()

final_output = agent.execute_objective("Investigate and resolve server latency spike on Node-4.")

print("\n--- Final Generated Deliverable ---")
print(final_output)
print("\nStatus: Plan-and-Solve cycle completed. Stepwise deterministic tracking verified.")