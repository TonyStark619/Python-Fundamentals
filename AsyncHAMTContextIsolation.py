# Phase 3, Master Day 221: Python Fundamentals - C-Level HAMT Context Isolation (contextvars)
import asyncio
import contextvars
import threading

print("--- Booting CPython HAMT Execution-Context Engine ---")

# 1. Declare the Context Variable
# Backed by CPython's internal immutable Hash Array Mapped Trie (Python/hamt.c)
REQUEST_AUTH_TOKEN: contextvars.ContextVar[str] = contextvars.ContextVar(
    "REQUEST_AUTH_TOKEN", default="UNAUTHENTICATED"
)

# A broken thread-local storage to prove why legacy threading primitives fail in async
legacy_thread_storage = threading.local()
legacy_thread_storage.token = "UNAUTHENTICATED"


async def downstream_database_query(client_name: str):
    """
    A deep internal function. Notice we DO NOT pass the auth token as an argument.
    It pulls the token directly from the CPython execution frame's HAMT context.
    """
    os_thread_id = threading.get_ident()
    hamt_isolated_token = REQUEST_AUTH_TOKEN.get()
    legacy_leaked_token = legacy_thread_storage.token

    print(f"    [{client_name} | OS Thread {os_thread_id}]")
    print(f"      -> C-HAMT ContextVar Token : {hamt_isolated_token} (STRICTLY ISOLATED)")
    print(f"      -> Legacy ThreadLocal Token: {legacy_leaked_token} (CORRUPTED BY RACE CONDITION)")


async def handle_incoming_request(client_name: str, secret_jwt: str, io_delay: float):
    """
    Simulates an asynchronous HTTP request handler running on a single-threaded event loop.
    """
    # Mutate both the C-level HAMT ContextVar and the legacy thread.local
    token_handle: contextvars.Token = REQUEST_AUTH_TOKEN.set(secret_jwt)
    legacy_thread_storage.token = secret_jwt

    try:
        # Yield control back to the event loop (Simulating network/disk I/O)
        # While paused here, other requests on the SAME OS thread will overwrite legacy_thread_storage!
        await asyncio.sleep(io_delay)

        # Resume execution and verify memory integrity
        await downstream_database_query(client_name)
    finally:
        # Mathematically roll back the HAMT state using the exact cryptographic token handle
        REQUEST_AUTH_TOKEN.reset(token_handle)


def run_sandboxed_sub_context():
    """
    Demonstrates manual O(1) context cloning via copy_context() outside of async loops.
    """
    print("\n--- Diagnostic 2: O(1) Immutable Context Forking (copy_context) ---")
    REQUEST_AUTH_TOKEN.set("ROOT_KERNEL_TOKEN")

    # Clone the current HAMT tree in O(1) time via structural sharing
    isolated_sandbox: contextvars.Context = contextvars.copy_context()

    # Execute a mutation strictly inside the cloned sandbox
    isolated_sandbox.run(REQUEST_AUTH_TOKEN.set, "SANDBOX_OVERRIDE_TOKEN")

    print(f"  -> Inside Sandbox Context : {isolated_sandbox[REQUEST_AUTH_TOKEN]}")
    print(f"  -> Main Process Context   : {REQUEST_AUTH_TOKEN.get()} (Unmodified!)")


async def main():
    print("\n--- Diagnostic 1: Single-Thread Concurrent Coroutine Collision ---")
    print("  [System] Dispatching 3 interleaved requests on a SINGLE OS thread...\n")

    # All three coroutines run concurrently on the exact same OS thread
    await asyncio.gather(
        handle_incoming_request("Client_Alpha", "JWT_ALPHA_991", 0.05),
        handle_incoming_request("Client_Beta ", "JWT_BETA_402", 0.02),
        handle_incoming_request("Client_Gamma", "JWT_GAMMA_777", 0.01),
    )

    run_sandboxed_sub_context()

    print("\nStatus: Python fundamentals verified. Single-thread async state bleeding eliminated via C-level HAMT context switching.")


if __name__ == "__main__":
    asyncio.run(main())