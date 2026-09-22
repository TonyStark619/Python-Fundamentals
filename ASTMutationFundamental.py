# Phase 3, Day 173: Python Fundamentals - Abstract Syntax Trees (AST)
import ast

print("--- Booting Compiler-Level AST Interceptor ---")

# 1. The Target Payload (Standard Python Code stored as a string)
source_code = """
def calculate_metrics(a, b):
    result = a + b
    return result
"""

print("\n[System] Original Source Code:")
print(source_code.strip())

# 2. Parse the raw string into an Abstract Syntax Tree
syntax_tree = ast.parse(source_code)

# 3. Define the Node Transformer (The Hijacker)
class OperatorMutator(ast.NodeTransformer):
    """
    Traverses the AST and replaces specific nodes. 
    In this case, we hunt for Binary Operations (BinOp).
    """
    def visit_BinOp(self, node):
        # We must call generic_visit first to traverse children nodes
        self.generic_visit(node)
        
        # If the operation is Addition, we mutate the node to Multiplication
        if isinstance(node.op, ast.Add):
            print("  [AST Intercept] Discovered ast.Add node. Mutating to ast.Mult...")
            # Create a brand new node replacing the operator
            return ast.BinOp(left=node.left, op=ast.Mult(), right=node.right)
            
        return node

# 4. Execute the Mutation
mutator = OperatorMutator()
mutated_tree = mutator.visit(syntax_tree)
# Fix missing line numbers required for compilation after mutation
ast.fix_missing_locations(mutated_tree)

# 5. Compile and Execute the hijacked tree in a new memory space
compiled_code = compile(mutated_tree, filename="<ast>", mode="exec")
execution_namespace = {}

print("\n[System] Compiling and loading mutated tree into memory...")
# Exec runs the compiled code block and stores the resulting function in execution_namespace
exec(compiled_code, execution_namespace)

# Extract the hijacked function
hijacked_function = execution_namespace['calculate_metrics']

print("\n--- Executing Hijacked Function ---")
test_a = 5
test_b = 10
print(f"Calling calculate_metrics({test_a}, {test_b})")
print(f"Expected addition result: {test_a + test_b}")

# The function will execute multiplication instead of addition
actual_result = hijacked_function(test_a, test_b)
print(f"CRITICAL RESULT: Payload executed with mutated logic -> {actual_result}")

print("\nStatus: Python fundamentals verified. AST compilation successfully hijacked and rewritten at runtime.")