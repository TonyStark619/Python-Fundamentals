# Phase 3, Master Day 229: Python Fundamentals - PyCodeObject Marshaling & Synthetic Closure Cells
import marshal
import types

print("--- Booting CPython Binary Code-Object Marshal & Closure-Cell Forge ---")


# 1. Factory creating a closure with two captured free variables ('multiplier' and 'audit_tag')
def build_template_closure(multiplier: int, audit_tag: str):
    def hot_settlement_kernel(amount: int) -> str:
        # 'multiplier' and 'audit_tag' are compiled as LOAD_DEREF instructions (Closure Cells)
        computed = amount * multiplier
        return f"[{audit_tag}] Settled Volume: {computed}"

    return hot_settlement_kernel


# --- Execution Environment ---

template_fn = build_template_closure(10, "LEGACY_TEMPLATE")

print("  [Compiler Forensics] Inspecting closure metadata on template function:")
print(f"    → Free Variables (co_freevars) : {template_fn.__code__.co_freevars}")
print(f"    → Original Closure Cells       : {[c.cell_contents for c in template_fn.__closure__]}")

print("\n--- Diagnostic 1: C-Level Binary Marshaling of PyCodeObject ---")
# marshal.dumps() serializes the raw CPython VM bytecode structure (used inside .pyc files)
raw_marshaled_bytecode: bytes = marshal.dumps(template_fn.__code__)
print(f"  → Serialized PyCodeObject Size   : {len(raw_marshaled_bytecode)} bytes")
print(f"  → Binary Header Hex              : {raw_marshaled_bytecode[:16].hex()}...")

# Reconstruct the compiled PyCodeObject directly from raw bytes
rehydrated_code_obj: types.CodeType = marshal.loads(raw_marshaled_bytecode)

print("\n--- Diagnostic 2: Synthesizing Custom Closure Cells via types.CellType ---")
# Notice we NEVER call build_template_closure() again!
# We forge raw C-level Cell objects directly matching co_freevars: ('audit_tag', 'multiplier')
cell_map = {
    "multiplier": types.CellType(250),
    "audit_tag": types.CellType("GUWAHATI_NODE_99"),
}
synthetic_closure_tuple = tuple(
    cell_map[var_name] for var_name in rehydrated_code_obj.co_freevars
)

# Dynamically assemble a live Python function from the marshaled code object + synthetic cells
forged_function = types.FunctionType(
    rehydrated_code_obj,
    globals(),
    name="forged_settlement_kernel",
    argdefs=(),
    closure=synthetic_closure_tuple,
)

print(f"  → Forged Function Execution(40)  : {forged_function(40)}")

print("\n--- Diagnostic 3: Live External Mutation of Private Closure Cell State ---")
# Mutate the C-level cell_contents pointer directly from the outside without re-creating the function
cell_map["multiplier"].cell_contents = 1000
cell_map["audit_tag"].cell_contents = "HOT_PATCHED_ENCLAVE"

print(f"  → Post-Cell-Mutation Execution(40): {forged_function(40)}")

print(
    "\nStatus: Python fundamentals verified. Raw PyCodeObjects marshaled and bound to synthetic types.CellType closures."
)