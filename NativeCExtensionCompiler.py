# Phase 3, Day 200: Python Fundamentals - Native C-Extension Compilation (Python.h)
import os
import subprocess
import sys

print("--- Booting Native C-Extension Compiler Architecture ---")

# 1. The Raw C-Code Payload
# This is physical C-language code, utilizing the CPython API to interface with Python objects.
c_extension_code = """
#include <Python.h>

// The native C function. It executes bypassing Python completely.
static PyObject* fast_power(PyObject* self, PyObject* args) {
    long long base, exponent;
    long long result = 1;

    // Parse the Python integers into native C 'long long' types
    if (!PyArg_ParseTuple(args, "LL", &base, &exponent)) {
        return NULL;
    }

    // Execute the math strictly at the hardware level
    for (long long i = 0; i < exponent; i++) {
        result *= base;
    }

    // Convert the native C result back into a Python Object to return it
    return PyLong_FromLongLong(result);
}

// Map the C function to the Python namespace
static PyMethodDef EnterpriseMathMethods[] = {
    {"fast_power", fast_power, METH_VARARGS, "Calculate power at native C speeds."},
    {NULL, NULL, 0, NULL}
};

// Define the Extension Module structure
static struct PyModuleDef enterprisemathmodule = {
    PyModuleDef_HEAD_INIT,
    "enterprise_math",
    "A C-Extension module for enterprise math operations.",
    -1,
    EnterpriseMathMethods
};

// The Initialization Hook CPython looks for when you run 'import enterprise_math'
PyMODINIT_FUNC PyInit_enterprise_math(void) {
    return PyModule_Create(&enterprisemathmodule);
}
"""

# 2. Write the C code to physical disk
c_filename = "enterprise_math.c"
with open(c_filename, "w") as f:
    f.write(c_extension_code)
print(f"  [System] Successfully generated physical C payload: {c_filename}")

# 3. Write the Setuptools build script
setup_code = """
from setuptools import setup, Extension
module = Extension('enterprise_math', sources=['enterprise_math.c'])
setup(name='EnterpriseMath', version='1.0', ext_modules=[module])
"""
setup_filename = "setup_c_ext.py"
with open(setup_filename, "w") as f:
    f.write(setup_code)
print(f"  [System] Successfully generated build instructions: {setup_filename}")

# --- Execution Environment ---

print("\n--- Invoking GCC/Clang Compiler via Setuptools ---")
try:
    # 4. We trigger the compiler via subprocess. 
    # This physically translates the C code into a .so or .pyd binary hardware library.
    subprocess.check_call([sys.executable, setup_filename, "build_ext", "--inplace"])
    print("  -> C-Extension successfully compiled into a native binary library.")
    
    print("\n--- Executing Native C Library Inside Python ---")
    
    # 5. Import the newly created binary just like a normal Python module
    import enterprise_math
    
    base_val = 5
    exp_val = 12
    print(f"Executing enterprise_math.fast_power({base_val}, {exp_val})...")
    
    # This call escapes the Python interpreter and hits the CPU hardware directly
    result = enterprise_math.fast_power(base_val, exp_val)
    
    print(f"\nCRITICAL RESULT: Hardware-level calculation completed successfully -> {result}")
    print("Status: Python boundary completely shattered. Native C integration dynamically compiled and executed.")

except subprocess.CalledProcessError:
    print("\n[ALERT] C-Compiler not found on host machine. (Ensure GCC or MSVC is installed in your system PATH).")
finally:
    # Cleanup the source files (Keep the compiled binary for proof)
    if os.path.exists(c_filename): os.remove(c_filename)
    if os.path.exists(setup_filename): os.remove(setup_filename)