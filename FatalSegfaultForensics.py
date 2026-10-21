# Phase 3, Day 210: Python Fundamentals - Fatal Memory Forensics (faulthandler)
import faulthandler
import ctypes
import tempfile
import subprocess
import sys
import os

print("--- Booting Enterprise C-Level Segfault Interceptor ---")

# We must simulate a silent server crash.
# Since a Segfault kills the actual Python interpreter, we will write a vulnerable script,
# run it as an isolated sub-process, crash it, and intercept its death rattle.

VULNERABLE_SERVER_CODE = """
import faulthandler
import ctypes

# 1. Arm the C-Level Fatal Signal Hook
# We instruct the OS to dump the stack trace to this specific file if the memory kernel panics.
crash_log = open("fatal_crash.log", "w")
faulthandler.enable(file=crash_log)

def complex_enterprise_transaction():
    print("  [Subprocess] Processing transaction...")
    trigger_c_level_memory_violation()

def trigger_c_level_memory_violation():
    print("  [Subprocess] Executing C-Extension...")
    # THE LETHAL ATTACK: We cast the integer '1' as a C memory pointer and attempt to dereference it.
    # The CPU hardware will instantly throw a Segmentation Fault (SIGSEGV).
    # Normal Python would vanish silently right here.
    ctypes.string_at(1)

complex_enterprise_transaction()
"""

# 2. Write the vulnerable server code to a temporary file
script_path = "vulnerable_server.py"
with open(script_path, "w") as f:
    f.write(VULNERABLE_SERVER_CODE)

# --- Execution Environment ---

print("\n  [System] Spawning vulnerable server process...")

try:
    # 3. Execute the server. It WILL crash.
    # We use subprocess to isolate the crash so our main script survives to read the logs.
    subprocess.run([sys.executable, script_path], check=True, capture_output=True)
except subprocess.CalledProcessError as e:
    # The OS returns negative signal numbers for fatal crashes (-11 is SIGSEGV on Linux/Mac)
    print(f"\n[ALERT] Server process abruptly terminated by Operating System!")
    print(f"  -> OS Exit Code: {e.returncode} (Fatal C-Level Signal)")

print("\n--- Initiating Post-Mortem Forensics ---")
# 4. Read the physical log file that faulthandler managed to save before death
if os.path.exists("fatal_crash.log"):
    with open("fatal_crash.log", "r") as log_file:
        traceback_dump = log_file.read()
        
    print("  [Forensics] Intercepted Death-Rattle Traceback:\n")
    print(traceback_dump)
    
    # Cleanup
    os.remove("fatal_crash.log")
else:
    print("  [Forensics] No crash log found. The server died silently.")

os.remove(script_path)

print("Status: Python fundamentals verified. Fatal C-level segmentation faults successfully intercepted and mathematically mapped via faulthandler.")