# Phase 3, Master Day 242: Python Fundamentals - PEP 669 Low-Impact VM Monitoring (sys.monitoring)
import sys
import types
from typing import List, Set

print("--- Booting CPython PEP 669 Low-Impact VM Instrumentation Engine ---")

if sys.version_info < (3, 12):
    raise RuntimeError("PEP 669 sys.monitoring requires Python 3.12 or newer.")

mon = sys.monitoring
ev = mon.events


# 1. Target Hot-Path Workload (Only this function's PyCodeObject will be instrumented!)
def compute_weighted_telemetry(iterations: int) -> int:
    accumulator = 0
    for idx in range(iterations):
        accumulator += (idx * 3) ^ 0x5A
    return accumulator


def unmonitored_peer_function(x: int) -> int:
    """Runs at 100% native speed because local events are never mounted on its code object."""
    return (x * x) + 17


# Telemetry Counters
call_starts: List[str] = []
return_values: List[int] = []
covered_lines: Set[int] = set()
line_callback_invocations: int = 0


# 2. PEP 669 Event Callbacks
def on_py_start(code: types.CodeType, instruction_offset: int):
    call_starts.append(f"{code.co_name}@offset:{instruction_offset}")


def on_py_return(code: types.CodeType, instruction_offset: int, retval: object):
    return_values.append(retval)


def on_line_one_shot(code: types.CodeType, line_number: int):
    """
    Records line coverage ONCE, then returns sys.monitoring.DISABLE so the CPython VM
    removes instrumentation from that exact bytecode location for all future iterations!
    """
    global line_callback_invocations
    line_callback_invocations += 1
    covered_lines.add(line_number)
    return mon.DISABLE


def acquire_free_tool_id(tool_name: str) -> int:
    """Safely claims an unused PEP 669 tool slot (0..5) to coexist with IDE debuggers."""
    for candidate_id in range(6):
        if mon.get_tool(candidate_id) is None:
            mon.use_tool_id(candidate_id, tool_name)
            return candidate_id
    raise RuntimeError("All 6 CPython sys.monitoring tool slots (0..5) are currently occupied.")


# --- Execution Environment ---

tool_id = acquire_free_tool_id("hot_path_pruning_profiler")
target_code = compute_weighted_telemetry.__code__
print(f"  [PEP 669 VM Hook] Claimed Tool Slot #{tool_id} ('{mon.get_tool(tool_id)}')")

try:
    # Register callbacks for PY_START, PY_RETURN, and LINE events
    mon.register_callback(tool_id, ev.PY_START, on_py_start)
    mon.register_callback(tool_id, ev.PY_RETURN, on_py_return)
    mon.register_callback(tool_id, ev.LINE, on_line_one_shot)

    # Surgically activate events ONLY on compute_weighted_telemetry.__code__
    mon.set_local_events(tool_id, target_code, ev.PY_START | ev.PY_RETURN | ev.LINE)

    print("\n--- Diagnostic 1: 10,000-Iteration Hot Loop with sys.monitoring.DISABLE Pruning ---")
    # Legacy sys.settrace() would fire 20,000+ line callbacks here; PEP 669 fires once per unique line!
    out_1 = compute_weighted_telemetry(10_000)
    _ = unmonitored_peer_function(42)  # Generates zero monitoring events

    print(f"  → Function Output (10,000 iters)   : {out_1:,}")
    print(f"  → Unique Lines Captured            : {sorted(covered_lines)}")
    print(f"  → Total LINE Callbacks Fired       : {line_callback_invocations} (Collapsed from 20,000+ via DISABLE!)")
    print(f"  → PY_START / PY_RETURN Captured    : {len(call_starts)} call(s) -> {return_values}")

    print("\n--- Diagnostic 2: Proving Persistent Zero-Overhead Bytecode Deactivation ---")
    before_second_run = line_callback_invocations
    _ = compute_weighted_telemetry(10_000)
    delta_second_run = line_callback_invocations - before_second_run

    print(f"  → Second 10,000-Iter LINE Callbacks: {delta_second_run} (Bytecode offsets remain uninstrumented!)")
    print(f"  → Total PY_START Calls Tracked     : {len(call_starts)} (Non-disabled events stay live!)")

    print("\n--- Diagnostic 3: Re-Arming Disabled Locations via sys.monitoring.restart_events() ---")
    mon.restart_events()
    before_rearm = line_callback_invocations
    _ = compute_weighted_telemetry(50)
    delta_after_rearm = line_callback_invocations - before_rearm

    print(f"  → Post-Restart LINE Callbacks Fired: {delta_after_rearm} (All disabled offsets cleanly re-armed!)")

finally:
    # Cleanly strip local events, unregister callbacks, and release the PEP 669 tool slot
    mon.set_local_events(tool_id, target_code, ev.NO_EVENTS)
    mon.register_callback(tool_id, ev.PY_START, None)
    mon.register_callback(tool_id, ev.PY_RETURN, None)
    mon.register_callback(tool_id, ev.LINE, None)
    mon.free_tool_id(tool_id)

print(
    "\nStatus: Python fundamentals verified. Per-code-object instrumentation and hot-path DISABLE pruning executed via PEP 669 sys.monitoring."
)