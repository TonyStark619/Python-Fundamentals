# Phase 3, Day 208: Python Fundamentals - Compiler Scope Forensics (symtable)
import symtable

print("--- Booting CPython Compiler Scope Forensics ---")

# 1. The Raw Target Code (Contains complex nested closures and globals)
TARGET_SOURCE_CODE = """
global_multiplier = 10

def outer_enterprise_function(x):
    closure_state = 5  # This variable is needed by the inner function
    
    def inner_worker(y):
        local_temp = 2
        # 'closure_state' is a FREE variable here, pulled from the outer scope
        # 'global_multiplier' is a GLOBAL variable
        return (x + y + closure_state + local_temp) * global_multiplier
        
    return inner_worker
"""

# 2. Extract the absolute Root Symbol Table from the compiler
print("  [Compiler] Generating Symbol Table for Source Code...")
root_table = symtable.symtable(TARGET_SOURCE_CODE, "<string>", "exec")

def analyze_scope(table, depth=0):
    """Recursively dissects the memory classification of every variable."""
    indent = "  " * depth
    print(f"\n{indent}--- Scope Isolated: '{table.get_name()}' (Type: {table.get_type()}) ---")
    
    # Analyze every variable (symbol) physically present in this scope
    for symbol in table.get_symbols():
        name = symbol.get_name()
        
        # Mathematical Memory Classifications
        is_global = symbol.is_global()
        is_local = symbol.is_local()
        # CELL: Exists in this scope, but an inner function relies on it
        is_cell = symbol.is_parameter() is False and symbol.is_local() and symbol.is_assigned() and table.has_children()
        # FREE: Does not exist in this scope, pulled from an outer wrapper function
        is_free = symbol.is_free()
        
        classification = []
        if is_global: classification.append("GLOBAL (Slow Hash Lookup)")
        if is_local: classification.append("LOCAL (Fast C-Array)")
        if symbol.is_parameter(): classification.append("PARAMETER")
        if is_free: classification.append("FREE (Closure Pointer Read)")
        
        # We manually infer Cell variables based on CPython behavior
        if not is_free and not is_global and name in [s.get_name() for child in table.get_children() for s in child.get_symbols() if s.is_free()]:
             classification.append("CELL (Closure Pointer Write)")

        print(f"{indent}  -> Variable: {name:<17} | Classification: {', '.join(classification)}")

    # Recursively dive into any nested functions or classes
    for child_table in table.get_children():
        analyze_scope(child_table, depth + 1)

# --- Execution Environment ---

print("\n[System] Commencing deep-dive variable lifecycle extraction...\n")
analyze_scope(root_table)

print("\nStatus: Python fundamentals verified. Variable memory lifecycles and closure mappings successfully extracted prior to bytecode compilation.")