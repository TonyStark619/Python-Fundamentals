# Phase 3, Master Day 227: Python Fundamentals - GC Phase Telemetry & Unraisable Destructor Traps
import gc
import sys
import time
from typing import Dict

print("--- Booting CPython GC Stop-The-World Telemetry & Unraisable Trap Engine ---")

# Store start timestamps per GC generation (0, 1, 2)
gc_phase_timers: Dict[int, int] = {}


# 1. CPython Generational GC Callback Hook (Modules/gcmodule.c)
def cpython_gc_phase_monitor(phase: str, info: Dict[str, int]) -> None:
    """
    Invoked directly by the CPython Garbage Collector at the 'start' and 'stop'
    of every generational stop-the-world collection pass.
    """
    gen = info["generation"]
    if phase == "start":
        gc_phase_timers[gen] = time.perf_counter_ns()
    elif phase == "stop":
        start_ns = gc_phase_timers.get(gen, time.perf_counter_ns())
        pause_us = (time.perf_counter_ns() - start_ns) / 1_000.0
        print(
            f"    [GC Kernel Telemetry] Generation-{gen} Sweep Complete | "
            f"Stop-The-World Pause: {pause_us:.2f} µs | "
            f"Reclaimed Cycles: {info['collected']} | "
            f"Uncollectable: {info['uncollectable']}"
        )


# 2. CPython Asynchronous Finalizer Fault Trap (sys.unraisablehook)
def enterprise_unraisable_fault_trap(unraisable: sys.UnraisableHookArgs) -> None:
    """
    Intercepts exceptions thrown inside __del__() destructors during garbage collection—
    exceptions that mathematically bypass all standard try/except blocks!
    """
    print(
        f"    [Unraisable Trap Triggered] Asynchronous destructor failure intercepted!\n"
        f"      → Faulting Object   : {repr(unraisable.object)}\n"
        f"      → Exception Type    : {unraisable.exc_type.__name__}\n"
        f"      → Exception Payload : {unraisable.exc_value}"
    )


# 3. Cyclic Socket Node with a Faulty Destructor
class CyclicClusterSession:
    def __init__(self, node_name: str, simulate_teardown_crash: bool = False):
        self.node_name = node_name
        self.peer_reference = None
        self.simulate_teardown_crash = simulate_teardown_crash

    def __repr__(self) -> str:
        return f"<CyclicClusterSession '{self.node_name}'>"

    def __del__(self):
        if self.simulate_teardown_crash:
            # This exception happens asynchronously inside the GC sweep!
            raise IOError(f"Hardware socket reset failed during teardown of {self.node_name}")


# --- Execution Environment ---

# Preserve original hooks for clean restoration
original_unraisable_hook = sys.unraisablehook

print("  [System] Mounting gc.callbacks and sys.unraisablehook into CPython runtime...")
gc.callbacks.append(cpython_gc_phase_monitor)
sys.unraisablehook = enterprise_unraisable_fault_trap

try:
    print("\n--- Diagnostic 1: Isolating Reference Cycles & Stop-The-World Pause Latency ---")
    # Disable automatic GC briefly so we can construct a deterministic cyclic graph
    gc.disable()

    node_alpha = CyclicClusterSession("GHY_NODE_ALPHA", simulate_teardown_crash=False)
    node_beta = CyclicClusterSession("GHY_NODE_BETA", simulate_teardown_crash=True)

    # Wire a bidirectional reference cycle (Reference count will NEVER hit 0 on del!)
    node_alpha.peer_reference = node_beta
    node_beta.peer_reference = node_alpha

    # Delete local pointers; objects survive in RAM as an isolated reference island
    del node_alpha
    del node_beta

    print("  [System] Local pointers deleted. Triggering Generation-2 GC collection sweep...\n")
    # Notice that wrapping gc.collect() in try/except would NEVER catch node_beta's __del__ IOError,
    # yet our sys.unraisablehook intercepts it cleanly while gc.callbacks measures the exact pause!
    reclaimed_objects = gc.collect(2)
    print(f"\n  → Total Cyclic Graph Objects Reclaimed by Gen-2 Sweep: {reclaimed_objects}")

finally:
    # Cleanly unregister our telemetry callback and restore default unraisable hook
    if cpython_gc_phase_monitor in gc.callbacks:
        gc.callbacks.remove(cpython_gc_phase_monitor)
    sys.unraisablehook = original_unraisable_hook
    gc.enable()

print("\nStatus: Python fundamentals verified. Stop-the-world GC pauses and uncatchable __del__ faults intercepted.")