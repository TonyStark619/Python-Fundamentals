# Phase 3, Master Day 237: Python Fundamentals - PEP 443 singledispatch & PEP 3119 __subclasshook__
from abc import ABC, abstractmethod
from functools import singledispatch
from typing import Tuple

print("--- Booting CPython PEP 443 Single-Dispatch & PEP 3119 Virtual Protocol Engine ---")


# 1. PEP 3119 Virtual Structural ABC
class ZeroCopyDeviceTensor(ABC):
    """
    Defines a structural contract WITHOUT requiring explicit inheritance.
    Any third-party class implementing 'device_shape' and 'to_device_bytes' is
    automatically recognized as a virtual subclass via __subclasshook__!
    """
    @property
    @abstractmethod
    def device_shape(self) -> Tuple[int, int]:
        ...

    @abstractmethod
    def to_device_bytes(self) -> bytes:
        ...

    @classmethod
    def __subclasshook__(cls, candidate_cls: type):
        # PEP 3119 guard: apply structural matching strictly to ZeroCopyDeviceTensor itself
        if cls is ZeroCopyDeviceTensor:
            has_shape = any("device_shape" in base.__dict__ for base in candidate_cls.__mro__)
            has_export = any("to_device_bytes" in base.__dict__ for base in candidate_cls.__mro__)
            if has_shape and has_export:
                return True
        return NotImplemented


# 2. Third-Party Hardware Class (ZERO inheritance from ZeroCopyDeviceTensor, ZERO .register() calls)
class ExternalAMDDeviceBuffer:
    """Simulates a sealed vendor SDK class whose source code we cannot modify."""
    def __init__(self, rows: int, cols: int, raw_payload: bytes):
        self._shape = (rows, cols)
        self._raw = raw_payload

    @property
    def device_shape(self) -> Tuple[int, int]:
        return self._shape

    def to_device_bytes(self) -> bytes:
        return self._raw


# 3. PEP 443 Open Single-Dispatch Generic Function
@singledispatch
def serialize_kernel_artifact(artifact: object) -> str:
    """Default fallback handler when no specialized type or virtual ABC matches."""
    return f"[Fallback Object] Type={type(artifact).__name__} -> repr={artifact!r}"


@serialize_kernel_artifact.register(bytes)
def _(artifact: bytes) -> str:
    return f"[Raw Bytes Handler] Payload={len(artifact)} bytes | Header=0x{artifact[:4].hex().upper()}"


@serialize_kernel_artifact.register(ZeroCopyDeviceTensor)
def _(artifact: ZeroCopyDeviceTensor) -> str:
    raw = artifact.to_device_bytes()
    return (
        f"[Virtual ABC Tensor Handler] Class={type(artifact).__name__} | "
        f"Shape={artifact.device_shape} | ContiguousBytes={len(raw)}"
    )


# --- Execution Environment ---

amd_buffer = ExternalAMDDeviceBuffer(1024, 512, b"\xDE\xAD\xBE\xEF" * 16)

print("\n--- Diagnostic 1: Verifying Zero-Inheritance Virtual Subtyping (PEP 3119) ---")
print(f"  → ExternalAMDDeviceBuffer.__mro__               : {ExternalAMDDeviceBuffer.__mro__}")
print(f"  → issubclass(..., ZeroCopyDeviceTensor)?        : {issubclass(ExternalAMDDeviceBuffer, ZeroCopyDeviceTensor)}")
print(f"  → isinstance(amd_buffer, ZeroCopyDeviceTensor)? : {isinstance(amd_buffer, ZeroCopyDeviceTensor)}")

print("\n--- Diagnostic 2: Executing Composed C3-MRO Generic Dispatch (PEP 443) ---")
print(f"  → Dispatch(bytes)          : {serialize_kernel_artifact(b'KERNEL_V237')}")
print(f"  → Dispatch(ExternalAMD)    : {serialize_kernel_artifact(amd_buffer)}")
print(f"  → Dispatch(unregistered)   : {serialize_kernel_artifact({'node': 'BPL_01'})}")

print("\n--- Diagnostic 3: Inspecting Internal Registry & Resolved MRO Cache ---")
resolved_handler = serialize_kernel_artifact.dispatch(ExternalAMDDeviceBuffer)
abc_handler = serialize_kernel_artifact.registry[ZeroCopyDeviceTensor]

print(f"  → Registered Concrete & ABC Keys : {[k.__name__ for k in serialize_kernel_artifact.registry.keys()]}")
print(f"  → ExternalAMD resolved directly to ABC handler? : {resolved_handler is abc_handler}")

print(
    "\nStatus: Python fundamentals verified. Third-party classes dispatched via PEP 3119 __subclasshook__ and cached in PEP 443 singledispatch."
)