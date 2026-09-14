# Phase 3, Day 56: Python Fundamentals - Concurrency via Asyncio
import asyncio
import time

print("--- Booting Python Fundamental Asynchronous Engine ---")

# 1. The Synchronous Bottleneck (Standard Python)
def sync_fetch_data(node_id):
    print(f"[Sync] Fetching data from Node {node_id}...")
    time.sleep(2) # Simulating a 2-second API block
    return f"Payload {node_id}"

def run_sync_execution():
    start = time.time()
    sync_fetch_data(1)
    sync_fetch_data(2)
    sync_fetch_data(3)
    print(f"-> Synchronous Execution Time: {time.time() - start:.2f} seconds\n")

# 2. The Asynchronous Architecture (Enterprise Standard)
async def async_fetch_data(node_id):
    print(f"[Async] Fetching data from Node {node_id}...")
    await asyncio.sleep(2) # Non-blocking wait. Surrenders control back to the event loop.
    return f"Payload {node_id}"

async def run_async_execution():
    start = time.time()
    # asyncio.gather fires all tasks concurrently and waits for them to finish
    results = await asyncio.gather(
        async_fetch_data(1),
        async_fetch_data(2),
        async_fetch_data(3)
    )
    print(f"-> Asynchronous Execution Time: {time.time() - start:.2f} seconds")
    print(f"-> Retrieved Data: {results}")

# --- Execution Environment ---
print("Executing Legacy Synchronous Sequence...")
run_sync_execution()

print("Executing Non-Blocking Asynchronous Sequence...")
# Python's event loop must be invoked to run async functions
asyncio.run(run_async_execution())

print("\nStatus: Python fundamentals verified. Concurrent I/O execution mathematically bypassed linear bottlenecks.")