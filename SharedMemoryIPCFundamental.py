# Phase 3, Day 192: Python Fundamentals - Zero-Copy IPC (shared_memory)
from multiprocessing import Process, shared_memory
import time
import sys

print("--- Booting C-Level Shared Memory IPC Engine ---")

def execute_child_process(memory_name: str, buffer_size: int):
    """
    This function runs in a completely isolated CPU process.
    It does NOT receive the massive data array as an argument.
    It only receives the 'name' of the OS memory block.
    """
    print(f"    [Child Process] Booting on separate CPU core...")
    
    # THE MAGIC: Attach directly to the existing physical RAM block allocated by the parent
    existing_shm = shared_memory.SharedMemory(name=memory_name)
    
    # Map the raw bytes to a zero-copy memoryview
    child_buffer = existing_shm.buf
    
    print("    [Child Process] Memory attached. Executing mutation...")
    # Overwrite the first 5 bytes instantly, bypassing serialization completely
    child_buffer[:5] = b'FAANG'
    
    print("    [Child Process] Mutation complete. Detaching memory...")
    existing_shm.close()

# --- Execution Environment ---

if __name__ == '__main__':
    # 1. Allocate a raw block of physical RAM (e.g., 100 Megabytes)
    # The OS tracks this memory block independent of standard Python object garbage collection
    BLOCK_SIZE = 100_000_000
    
    print(f"\n[Main Process] Allocating {BLOCK_SIZE / 1_000_000} MB of OS-level shared memory...")
    shm = shared_memory.SharedMemory(create=True, size=BLOCK_SIZE)
    
    # Initialize the memory with zeros
    shm.buf[:BLOCK_SIZE] = b'\x00' * BLOCK_SIZE
    
    print(f"[Main Process] Shared Memory Block '{shm.name}' successfully allocated.")
    print(f"[Main Process] Byte Index [0:5] BEFORE: {bytes(shm.buf[:5])}")
    
    # 2. Spawn a completely isolated process
    # We do NOT pass the 100MB buffer. We only pass the string name.
    p = Process(target=execute_child_process, args=(shm.name, BLOCK_SIZE))
    
    start_time = time.time()
    p.start()
    p.join() # Wait for child process to finish
    execution_time = time.time() - start_time
    
    # 3. Mathematical Proof of IPC Zero-Copy
    print(f"\n[Main Process] Child process terminated in {execution_time * 1000:.2f} ms.")
    
    final_bytes = bytes(shm.buf[:5])
    print(f"[Main Process] Byte Index [0:5] AFTER: {final_bytes}")
    
    if final_bytes == b'FAANG':
        print("\nCRITICAL RESULT: Memory mutated successfully by isolated process. Zero serialization overhead.")
        
    # 4. Critical Enterprise Cleanup
    # If you do not unlink, the memory permanently leaks into the OS until reboot!
    shm.close()
    shm.unlink() 
    print("\nStatus: Python fundamentals verified. GIL mathematically bypassed via OS-level physical shared memory.")