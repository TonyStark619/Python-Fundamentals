# Phase 3, Master Day 238: Python Fundamentals - Heap Generator Frames, .throw() & Stackless Trampolines
import inspect
import sys

print("--- Booting CPython Heap-Frame Coroutine & Stackless Trampoline Engine ---")


# 1. Bi-Directional Resumable State Machine (PEP 342 Protocol)
def resilient_ledger_accumulator(initial_balance: int):
    """
    Executes inside a heap-allocated PyGenObject frame.
    Supports live .send() ingestion, mid-suspension .throw() fault recovery,
    and deterministic GeneratorExit teardown via .close().
    """
    running_total = initial_balance
    faults_recovered = 0
    try:
        while True:
            try:
                # Pause execution here, yielding current state and awaiting injected delta
                incoming_delta = yield running_total
                if incoming_delta is not None:
                    running_total += incoming_delta
            except ValueError as injected_fault:
                faults_recovered += 1
                print(
                    f"    [Inside Suspended Frame] Intercepted .throw() fault: {injected_fault} "
                    f"(Total recovered: {faults_recovered})"
                )
    finally:
        print(
            f"    [Deterministic Teardown] GeneratorExit received -> Final Balance={running_total}, "
            f"Faults Absorbed={faults_recovered}."
        )


# 2. Stackless Recursive Generator Step (O(1) Physical Call Stack Depth)
def stackless_deep_accumulator(remaining_steps: int, acc: int = 0):
    """
    Instead of pushing a new frame onto the CPython call stack, yields the next
    continuation generator to the trampoline driver.
    """
    if remaining_steps == 0:
        # Capture actual physical call-stack height at logical recursion depth 50,000!
        physical_stack_height = len(inspect.stack())
        return acc, physical_stack_height

    # Yielding transfers control back to the trampoline so this frame is freed immediately
    yield stackless_deep_accumulator(remaining_steps - 1, acc + remaining_steps)


def run_stackless_trampoline(initial_continuation):
    """Flat O(1)-stack driver loop consuming yielded generator continuations."""
    current = initial_continuation
    while True:
        try:
            current = next(current)
        except StopIteration as finished:
            return finished.value


# --- Execution Environment ---

print("\n--- Diagnostic 1: Live PyGenObject Frame Forensics & .throw() Injection ---")
ledger_gen = resilient_ledger_accumulator(1000)

print(f"  → Initial Lifecycle State   : {inspect.getgeneratorstate(ledger_gen)}")
# Prime generator up to its first 'yield'
initial_out = next(ledger_gen)
print(
    f"  → Primed Output             : {initial_out} | State: {inspect.getgeneratorstate(ledger_gen)} "
    f"| Bytecode Offset (f_lasti): {ledger_gen.gi_frame.f_lasti}"
)

# Push values directly into the paused yield expression via .send()
updated_out = ledger_gen.send(450)
print(
    f"  → After .send(450)          : {updated_out} | Live Heap Frame Locals: "
    f"{ledger_gen.gi_frame.f_locals}"
)

# Surgically throw a ValueError straight into the suspended heap frame!
post_fault_out = ledger_gen.throw(ValueError("Malformed checksum on inbound tranche"))
print(f"  → Resumed Post-Fault Balance: {post_fault_out} (Frame survived intact!)")

# Trigger deterministic GeneratorExit cleanup
ledger_gen.close()
print(
    f"  → Post-.close() State       : {inspect.getgeneratorstate(ledger_gen)} "
    f"| gi_frame is None? {ledger_gen.gi_frame is None}"
)


print("\n--- Diagnostic 2: Executing 50,000-Depth Recursion via O(1)-Stack Trampoline ---")
TARGET_DEPTH = 50_000
current_limit = sys.getrecursionlimit()

total_sum, observed_stack_frames = run_stackless_trampoline(
    stackless_deep_accumulator(TARGET_DEPTH)
)
expected_gauss_sum = TARGET_DEPTH * (TARGET_DEPTH + 1) // 2

print(f"  → CPython Hard Recursion Limit  : {current_limit:,} frames")
print(f"  → Logical Recursion Executed    : {TARGET_DEPTH:,} steps (50x past stack limit!)")
print(f"  → Physical Call-Stack Depth     : {observed_stack_frames} frames (Strictly O(1)!)")
print(f"  → Computed Sum vs Gauss Formula : {total_sum:,} == {expected_gauss_sum:,} (Exact Match: {total_sum == expected_gauss_sum})")

print(
    "\nStatus: Python fundamentals verified. Heap generator frames driven via PEP 342 .send()/.throw() and O(1)-stack trampolines."
)