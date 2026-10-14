# Phase 3, Day 202: Python Fundamentals - AST Syntax Rewriting (ast.NodeTransformer)
import ast

print("--- Booting CPython Compiler Macro Engine ---")

# 1. The Raw Human Code
# Notice the developer clearly wrote ADDITION (+)
original_code_string = """
def enterprise_calculation(x, y):
    return x + y
"""

print("  [System] Original Code Submitted to Compiler:")
print(original_code_string.strip())

# 2. Parse the string into a mathematical syntax tree
abstract_syntax_tree = ast.parse(original_code_string)


# 3. The Interceptor: Custom Node Transformer
class MathematicsHacker(ast.NodeTransformer):
    """
    This class walks the AST. Whenever it encounters a specific type of node,
    it executes a callback that allows us to physically replace the node before compilation.
    """
    
    # Intercept every Binary Operation (Math)
    def visit_BinOp(self, node):
        # We must visit the children first in case there are nested operations
        self.generic_visit(node)
        
        # If the operation is Addition...
        if isinstance(node.op, ast.Add):
            print("  [Macro Hook] Intercepted an ast.Add node. Mutating tree to ast.Mult...")
            # We construct a brand new Node and return it to overwrite the old one
            new_node = ast.BinOp(
                left=node.left,
                op=ast.Mult(),  # <--- THE HACK: Changing '+' to '*'
                right=node.right
            )
            # Carry over the line numbers so the compiler doesn't crash
            return ast.copy_location(new_node, node)
        
        # Return the unmodified node if it wasn't Addition
        return node


# --- Execution Environment ---

print("\n--- Initiating AST Traversal and Mutation ---")
# Feed the tree through our hacker class
mutated_tree = MathematicsHacker().visit(abstract_syntax_tree)

# Fix locations in case we generated new nodes without line numbers
ast.fix_missing_locations(mutated_tree)

print("  [System] AST successfully mutated. Engaging CPython compiler...")

# 4. Compile the mutated tree directly into raw bytecode
compiled_bytecode = compile(mutated_tree, filename="<macro_engine>", mode="exec")

# 5. Execute the bytecode into a namespace so we can call the function
execution_namespace = {}
exec(compiled_bytecode, execution_namespace)

# Extract the function
hacked_function = execution_namespace['enterprise_calculation']

print("\n--- Executing Mutated Logic ---")
test_x = 10
test_y = 5
print(f"Calling enterprise_calculation({test_x}, {test_y})...")

# The developer wrote 'x + y' (Expecting 15)
# The compiler executes 'x * y' (Resulting in 50)
result = hacked_function(test_x, test_y)

print(f"\nCRITICAL RESULT: Payload executed -> {result}")
print("Status: Python fundamentals verified. Source logic structurally rewritten via pre-compilation AST Node Transformers.")