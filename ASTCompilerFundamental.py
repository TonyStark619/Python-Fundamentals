# Phase 3, Day 186: Python Fundamentals - AST Synthesis & Compilation
import ast

print("--- Booting CPython Abstract Syntax Tree Synthesizer ---")

# 1. We are going to build this function entirely out of mathematical nodes, not strings:
# def dynamic_multiplier(x, y):
#     return x * y

print("  [System] Forging geometric AST nodes in RAM...")

# Define the arguments (x, y)
args_node = ast.arguments(
    posonlyargs=[],
    args=[ast.arg(arg='x'), ast.arg(arg='y')],
    kwonlyargs=[], kw_defaults=[], defaults=[]
)

# Define the mathematical operation (x * y)
multiply_node = ast.BinOp(
    left=ast.Name(id='x', ctx=ast.Load()),
    op=ast.Mult(),
    right=ast.Name(id='y', ctx=ast.Load())
)

# Define the Return statement wrapping the math operation
return_node = ast.Return(value=multiply_node)

# Wrap it all inside a Function Definition
function_node = ast.FunctionDef(
    name='dynamic_multiplier',
    args=args_node,
    body=[return_node],
    decorator_list=[]
)

# Wrap the function inside a top-level Module
module_node = ast.Module(body=[function_node], type_ignores=[])

# 2. Fix locations (CPython requires line numbers and column offsets to compile)
ast.fix_missing_locations(module_node)

print("  [System] AST construction complete. Engaging compiler...")

# 3. Compile the pure AST object directly into raw CPython Bytecode
# mode='exec' tells Python we are compiling a block of statements (like a script file)
compiled_bytecode = compile(module_node, filename="<ast_factory>", mode="exec")

# 4. Create an isolated namespace (RAM block) and execute the bytecode to materialize it
execution_namespace = {}
exec(compiled_bytecode, execution_namespace)

print("\n--- Executing Synthesized Logic ---")
# Extract the newly forged function from the memory space
forged_function = execution_namespace['dynamic_multiplier']

test_val_1 = 15
test_val_2 = 4
print(f"Calling forged_function({test_val_1}, {test_val_2})...")

# It executes at full native Python speed because it was properly compiled
result = forged_function(test_val_1, test_val_2)
print(f"CRITICAL RESULT: Payload executed successfully -> {result}")

print("\nStatus: Python fundamentals verified. Executable memory dynamically synthesized from raw AST nodes without string parsing.")