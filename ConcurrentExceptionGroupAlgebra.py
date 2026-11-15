# Phase 3, Master Day 234: Python Fundamentals - PEP 654 ExceptionGroup Algebra & except* Unwinding
import sys

print("--- Booting CPython PEP 654 Concurrent ExceptionGroup & except* Engine ---")


# 1. Custom Domain Exceptions for a Scatter-Gather Cluster Fan-Out
class RetryableShardError(Exception):
    def __init__(self, shard_id: str, latency_ms: int):
        self.shard_id = shard_id
        self.latency_ms = latency_ms
        super().__init__(f"Shard '{shard_id}' timed out after {latency_ms} ms")


class FatalEnclaveBreachError(PermissionError):
    def __init__(self, node_id: str):
        self.node_id = node_id
        super().__init__(f"Attestation signature rejected on '{node_id}'")


class CorruptPayloadSchemaError(ValueError):
    pass


def build_nested_cluster_failure_tree() -> ExceptionGroup:
    """
    Simulates a hierarchical scatter-gather fan-out where Regional Cluster A and Regional Cluster B
    fail concurrently with heterogeneous leaf exceptions.
    """
    region_alpha_failures = ExceptionGroup(
        "Region_Alpha_Fanout_Failures",
        [
            RetryableShardError("GHY_SHARD_01", 1450),
            FatalEnclaveBreachError("GHY_ENCLAVE_CORE"),
        ],
    )

    region_beta_failures = ExceptionGroup(
        "Region_Beta_Fanout_Failures",
        [
            RetryableShardError("BLR_SHARD_04", 2100),
            CorruptPayloadSchemaError("Malformed protobuf header at byte offset 12"),
        ],
    )

    return ExceptionGroup(
        "Global_Scatter_Gather_Collapse",
        [region_alpha_failures, region_beta_failures],
    )


# --- Execution Environment ---

failure_tree = build_nested_cluster_failure_tree()

print("\n--- Diagnostic 1: Functional Tree Partitioning via .split(predicate) ---")
# .split() partitions the nested ExceptionGroup tree into (matched_subtree, unmatched_subtree)
# using either an exception type tuple OR a custom callable predicate!
high_latency_retries, remaining_faults = failure_tree.split(
    lambda exc: isinstance(exc, RetryableShardError) and exc.latency_ms > 1000
)

print(f"  → Isolated Retryable Subtree : {high_latency_retries!r}")
for sub_group in high_latency_retries.exceptions:
    print(f"      * {sub_group.message} -> {sub_group.exceptions}")

print(f"  → Remaining Non-Retryable    : {remaining_faults!r}")


print("\n--- Diagnostic 2: Multi-Branch Selective Unwinding via except* ---")
# Notice: In standard Python try/except, ONLY the first matching except block ever executes.
# With PEP 654 except*, EVERY matching handler block executes on its respective slice of the tree!

handled_categories = []

try:
    raise failure_tree
except* RetryableShardError as retry_eg:
    # Captures ALL RetryableShardErrors across both Region Alpha and Region Beta simultaneously
    handled_categories.append("RETRY_QUEUE")
    print(f"  [except* Branch 1 Fired] Queued {len(retry_eg.exceptions)} regional retry subtrees:")
    for reg in retry_eg.exceptions:
        for leaf in reg.exceptions:
            print(f"    → Scheduling backoff retry for: {leaf}")

except* FatalEnclaveBreachError as security_eg:
    # Captures ALL FatalEnclaveBreachErrors in the exact same try block pass!
    handled_categories.append("SECURITY_LOCKDOWN")
    print(f"  [except* Branch 2 Fired] Quarantined compromised enclave nodes:")
    for reg in security_eg.exceptions:
        for leaf in reg.exceptions:
            print(f"    → Isolating node: {leaf}")

except* CorruptPayloadSchemaError as schema_eg:
    # Captures ALL CorruptPayloadSchemaErrors in the exact same try block pass!
    handled_categories.append("DEAD_LETTER_QUEUE")
    print(f"  [except* Branch 3 Fired] Routed malformed payloads to Dead-Letter Queue:")
    for reg in schema_eg.exceptions:
        for leaf in reg.exceptions:
            print(f"    → Quarantined schema fault: {leaf}")

print(f"\n  → Verified Handler Branches Executed in Single Raise : {handled_categories}")
print("Status: Python fundamentals verified. Concurrent fault trees partitioned and unwound via PEP 654 ExceptionGroup and except*.")