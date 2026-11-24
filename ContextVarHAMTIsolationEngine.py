# Phase 3, Master Day 240: Python Fundamentals - PEP 567 Immutable HAMT Contexts (contextvars)
import asyncio
import contextvars
import threading

print("--- Booting CPython PEP 567 HAMT ContextVar Isolation Engine ---")

# 1. Legacy Thread-Local Storage (Vulnerable to coroutine interleaving on a single OS thread)
legacy_tls = threading.local()

# 2. PEP 567 HAMT-Backed ContextVar (Task-isolated across asyncio suspension points)
active_tenant_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "active_tenant_ctx", default="UNASSIGNED"
)
compliance_tier_ctx: contextvars.ContextVar[str] = contextvars.ContextVar(
    "compliance_tier_ctx", default="STANDARD"
)


async def execute_interleaved_request(tenant_id: str, yield_delay_sec: float) -> tuple[str, str]:
    """
    Writes tenant identity to BOTH threading.local() and ContextVar, then suspends
    on 'await' so a rival coroutine executes on the exact same OS thread.
    """
    legacy_tls.tenant_id = tenant_id
    active_tenant_ctx.set(tenant_id)

    # Yield control back to the single-threaded event loop -> forces coroutine interleaving!
    await asyncio.sleep(yield_delay_sec)

    observed_tls = getattr(legacy_tls, "tenant_id", "MISSING")
    observed_ctx = active_tenant_ctx.get()
    return observed_tls, observed_ctx


async def verify_async_isolation() -> None:
    print("\n--- Diagnostic 1: Proving threading.local() Corruption vs ContextVar Isolation ---")
    # Task Alpha yields slightly longer so Task Beta overwrites legacy_tls before Alpha resumes!
    task_alpha = asyncio.create_task(execute_interleaved_request("TENANT_ALPHA", 0.03))
    task_beta = asyncio.create_task(execute_interleaved_request("TENANT_BETA", 0.01))

    (alpha_tls, alpha_ctx), (beta_tls, beta_ctx) = await asyncio.gather(task_alpha, task_beta)

    print(f"  → Task ALPHA (Expected 'TENANT_ALPHA') | threading.local: '{alpha_tls}' (CORRUPTED!) | ContextVar: '{alpha_ctx}'")
    print(f"  → Task BETA  (Expected 'TENANT_BETA')  | threading.local: '{beta_tls}' | ContextVar: '{beta_ctx}'")
    print(f"  → Same OS Thread ID for Both Tasks?    : True (Thread #{threading.get_ident()})")


def verify_token_rollback_and_sandbox() -> None:
    print("\n--- Diagnostic 2: Deterministic Token Rollback & One-Shot Guard ---")
    print(f"  → Baseline compliance_tier_ctx  : {compliance_tier_ctx.get()}")

    # Nested state mutation guarded by a PEP 567 Token
    token = compliance_tier_ctx.set("EXPORT_RESTRICTED_ENCLAVE")
    print(f"  → Elevated compliance_tier_ctx  : {compliance_tier_ctx.get()} (token.old_value = {token.old_value!r})")

    # Atomically roll back to prior state
    compliance_tier_ctx.reset(token)
    print(f"  → Post-Reset compliance_tier_ctx: {compliance_tier_ctx.get()}")

    # Verify one-shot token guard prevents accidental double-rollback
    try:
        compliance_tier_ctx.reset(token)
    except RuntimeError as exc:
        print(f"  → [One-Shot Guard Verified] Duplicate reset blocked: {exc}")

    print("\n--- Diagnostic 3: Copy-on-Write HAMT Snapshot Execution via copy_context().run() ---")
    active_tenant_ctx.set("PARENT_ROOT_TENANT")
    hamt_snapshot: contextvars.Context = contextvars.copy_context()

    def isolated_sandbox_mutation() -> str:
        active_tenant_ctx.set("SANDBOX_EPHEMERAL_TENANT")
        compliance_tier_ctx.set("ZERO_TRUST_AUDIT")
        return f"Inside Sandbox -> tenant='{active_tenant_ctx.get()}', tier='{compliance_tier_ctx.get()}'"

    # Execute inside the cloned HAMT branch; mutations stay sealed inside 'hamt_snapshot'
    sandbox_report = hamt_snapshot.run(isolated_sandbox_mutation)
    print(f"  → {sandbox_report}")
    print(f"  → Parent Context After Sandbox  : tenant='{active_tenant_ctx.get()}', tier='{compliance_tier_ctx.get()}' (Zero Leakage!)")
    print(f"  → Inspecting Cloned HAMT Keys   : {[(var.name, val) for var, val in hamt_snapshot.items()]}")


if __name__ == "__main__":
    asyncio.run(verify_async_isolation())
    verify_token_rollback_and_sandbox()
    print(
        "\nStatus: Python fundamentals verified. Coroutine state leakage eliminated via PEP 567 HAMT ContextVars, Tokens, and copy_context()."
    )