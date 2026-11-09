# Phase 3, Master Day 228: Python Fundamentals - Lexical Token-Stream Interception (tokenize)
import io
import token
import tokenize
from decimal import Decimal
from typing import List, Tuple

print("--- Booting CPython Stage-1 Lexical Token-Stream Transpiler ---")


def transpile_floats_to_exact_decimal(source_code: str) -> str:
    """
    Intercepts the raw lexical token stream BEFORE AST parsing.
    Rewrites every floating-point NUMBER literal (e.g., 0.1) into Decimal('0.1')
    so IEEE-754 binary float rounding never touches the compilation pipeline.
    """
    byte_stream = io.BytesIO(source_code.encode("utf-8"))
    raw_tokens = tokenize.tokenize(byte_stream.readline)

    transformed_tokens: List[Tuple[int, str]] = []

    for tok_type, tok_string, _start, _end, _line in raw_tokens:
        # Intercept lexical NUMBER tokens containing a decimal point or scientific exponent
        if tok_type == token.NUMBER and ("." in tok_string or "e" in tok_string.lower()):
            print(
                f"    [Lexer Hook] Intercepted float literal '{tok_string}' -> "
                f"Rewriting token stream to Decimal('{tok_string}')"
            )
            transformed_tokens.extend(
                [
                    (token.NAME, "Decimal"),
                    (token.OP, "("),
                    (token.STRING, repr(tok_string)),
                    (token.OP, ")"),
                ]
            )
        else:
            transformed_tokens.append((tok_type, tok_string))

    # Reconstruct valid Python source code from the mutated lexical token stream
    reconstructed_bytes = tokenize.untokenize(transformed_tokens)
    return reconstructed_bytes.decode("utf-8")


# --- Execution Environment ---

# Simulated financial settlement formula written with standard float literals
FINTECH_SETTLEMENT_SCRIPT = """
def calculate_gst_settlement():
    tranche_alpha = 0.1
    tranche_beta = 0.2
    total_tax = tranche_alpha + tranche_beta
    return total_tax
"""

print("\n--- Diagnostic 1: Standard IEEE-754 Binary Float Compilation ---")
legacy_namespace = {}
exec(FINTECH_SETTLEMENT_SCRIPT, legacy_namespace)
legacy_result = legacy_namespace["calculate_gst_settlement"]()

print(f"  → Standard Execution (0.1 + 0.2) : {legacy_result!r}")
print(f"  → Exact Equality to 0.3?         : {legacy_result == 0.3}")

print("\n--- Diagnostic 2: Lexical Token-Stream Interception & Recompilation ---")
transpiled_source = transpile_floats_to_exact_decimal(FINTECH_SETTLEMENT_SCRIPT)

print("\n  [Transpiled Source Output]:")
for line in transpiled_source.strip().splitlines():
    print(f"    {line}")

hermetic_namespace = {"Decimal": Decimal}
exec(transpiled_source, hermetic_namespace)
exact_result = hermetic_namespace["calculate_gst_settlement"]()

print(f"\n  → Lexer-Transpiled Result        : {exact_result!r} (Type: {type(exact_result).__name__})")
print(f"  → Exact Equality to Decimal(0.3) : {exact_result == Decimal('0.3')}")

print(
    "\nStatus: Python fundamentals verified. IEEE-754 float drift eliminated at Stage-1 lexical tokenization prior to AST construction."
)