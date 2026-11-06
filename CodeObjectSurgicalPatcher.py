# Phase 3, Master Day 224: Python Fundamentals - PyCodeObject Surgical Patching (__code__.replace)
import types

print("--- Booting CPython PyCodeObject Surgical Specialization Engine ---")


# 1. Target Hot-Path Kernel
# Notice that 1000 and 0.18 are compiled directly into the function's co_consts tuple
def compute_settlement_margin(volume: int) -> float:
    base_offset = 1000
    tariff_multiplier = 0.18
    return (volume + base_offset) * tariff_multiplier


def inspect_code_object_internals(func: types.FunctionType, label: str):
    code_obj = func.__code__
    print(f"\n  [{label}] PyCodeObject Forensics for '{func.__name__}()':")
    print(f"    → co_varnames (Local C-Array) : {code_obj.co_varnames}")
    print(f"    → co_consts   (Literal Pool)  : {code_obj.co_consts}")
    print(f"    → co_stacksize (VM Stack)     : {code_obj.co_stacksize}")


def surgically_specialize_constants(
    func: types.FunctionType, old_const, new_const
) -> None:
    """
    Mutates a compiled function's internal constant pool in-place using __code__.replace().
    Zero wrapper frames, zero eval/exec compilation, zero global dictionary lookups.
    """
    original_code: types.CodeType = func.__code__

    # Reconstruct the co_consts tuple, swapping the target constant
    mutated_consts = tuple(
        new_const if c == old_const else c for c in original_code.co_consts
    )

    # THE MAGIC: Forge a new C-level PyCodeObject with the updated constant table
    # and bind it directly back to the existing function object!
    func.__code__ = original_code.replace(co_consts=mutated_consts)
    print(
        f"    -> [Kernel Patch] Swapped literal constant {old_const} -> {new_const} inside '{func.__name__}.__code__'"
    )


# --- Execution Environment ---

inspect_code_object_internals(compute_settlement_margin, "Baseline Compilation")

baseline_output = compute_settlement_margin(500)
print(f"  → Baseline Execution compute_settlement_margin(500) = {baseline_output:.2f}")

print("\n--- Executing Zero-Wrapper Surgical Constant Specialization ---")
# Dynamically specialize the compiled function's constants in RAM:
# Change base_offset (1000 -> 5000) and tariff_multiplier (0.18 -> 0.25)
surgically_specialize_constants(compute_settlement_margin, 1000, 5000)
surgically_specialize_constants(compute_settlement_margin, 0.18, 0.25)

inspect_code_object_internals(compute_settlement_margin, "Post-Patch Specialization")

specialized_output = compute_settlement_margin(500)
# Expected: (500 + 5000) * 0.25 = 1375.00
print(f"  → Specialized Execution compute_settlement_margin(500) = {specialized_output:.2f}")

print(
    "\nStatus: Python fundamentals verified. Compiled function constants mutated in-place via PyCodeObject.replace() with zero decorator frame overhead."
)