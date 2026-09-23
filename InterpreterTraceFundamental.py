# Phase 3, Day 174: Python Fundamentals - Interpreter Level Tracing (sys.settrace)
import sys

print("--- Booting CPython Interpreter Trace Hook ---")

# 1. Define the Spy (The Trace Hook)
def execution_tracer(frame, event, arg):
    """
    This function is called by the Python interpreter on EVERY line of execution.
    frame: The current execution frame (holds variables and line numbers).
    event: What is happening ('call', 'line', 'return', 'exception').
    arg: Additional context (like return values).
    """
    # Extract the name of the function currently executing
    func_name = frame.f_code.co_name
    
    # We only want to trace our specific target functions, not Python's internal booting
    if func_name == "calculate_compound_logic":
        line_no = frame.f_lineno
        
        if event == 'call':
            print(f"  [TRACE: CALL]   -> Entering {func_name}() at line {line_no}")
        
        elif event == 'line':
            # We can literally read the live local variables at this exact microsecond
            locals_state = frame.f_locals
            print(f"  [TRACE: LINE]   -> Executing line {line_no} | State: {locals_state}")
            
        elif event == 'return':
            print(f"  [TRACE: RETURN] -> Exiting {func_name}() with value: {arg}")
            
    return execution_tracer

# 2. A target function containing logic we want to monitor
def calculate_compound_logic(base, multiplier):
    total = base
    for i in range(2):
        total += (total * multiplier)
    return total

# --- Execution Environment ---
print("\n[System] Injecting custom trace hook into the interpreter...\n")
# Activate the global trace
sys.settrace(execution_tracer)

# Execute the code - our hook will intercept every single operation
result = calculate_compound_logic(10, 0.5)

# Immediately disable the trace to prevent massive overhead on the rest of the script
sys.settrace(None)

print(f"\nCRITICAL RESULT: Final payload output -> {result}")
print("Status: Python fundamentals verified. Interpreter execution loop successfully intercepted and logged.")