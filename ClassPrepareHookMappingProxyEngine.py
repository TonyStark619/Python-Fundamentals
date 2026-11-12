# Phase 3, Master Day 231: Python Fundamentals - PEP 3115 __prepare__ & C-Level MappingProxyType
import types

print("--- Booting CPython PEP 3115 __prepare__ & MappingProxyType Engine ---")


# 1. Custom Class-Body Execution Namespace
class WriteOnceClassNamespace(dict):
    """
    Injected by __prepare__ as the live local dictionary while a class body executes.
    Intercepts every STORE_NAME bytecode instruction inside the class definition block!
    """
    def __init__(self, class_name: str):
        super().__init__()
        self.class_name = class_name
        self.declaration_order = []

    def __setitem__(self, key: str, value: object):
        # Allow standard compiler metadata attributes (__module__, __qualname__, __doc__)
        if key in self and not (key.startswith("__") and key.endswith("__")):
            raise SyntaxError(
                f"PEP 3115 COLLISION TRAP: Duplicate definition of '{key}' detected inside "
                f"class '{self.class_name}'. Silent method shadowing is strictly prohibited!"
            )
        if not key.startswith("__"):
            self.declaration_order.append(key)
        super().__setitem__(key, value)


# 2. Metaclass Implementing PEP 3115 __prepare__
class CollisionProofMeta(type):
    @classmethod
    def __prepare__(mcs, name: str, bases: tuple, **kwargs):
        print(f"  [PEP 3115 __prepare__] Mounting WriteOnceClassNamespace for class '{name}'...")
        return WriteOnceClassNamespace(name)

    def __new__(mcs, name: str, bases: tuple, namespace: WriteOnceClassNamespace, **kwargs):
        cls = super().__new__(mcs, name, bases, dict(namespace))
        # Expose the declaration order as an immutable tuple
        cls.__declaration_order__ = tuple(namespace.declaration_order)
        return cls


# --- Execution Environment ---

print("\n--- Diagnostic 1: Compiling a Valid Enterprise Service Class ---")
class SettlementGateway(metaclass=CollisionProofMeta):
    PROTOCOL_VERSION = 4

    def authorize_tranche(self, amount: int) -> bool:
        return amount > 0

    def commit_ledger(self) -> str:
        return "COMMITTED"


print(f"  → Verified Declaration Order : {SettlementGateway.__declaration_order__}")
print(f"  → Class __dict__ Type        : {type(SettlementGateway.__dict__)} (C-level mappingproxy)")


print("\n--- Diagnostic 2: Trapping Silent Method Shadowing Inside a Class Body ---")
try:
    class CorruptedGateway(metaclass=CollisionProofMeta):
        def verify_signature(self) -> bool:
            return True

        # In standard Python, this second definition silently overwrites the first!
        # With __prepare__, CPython aborts at the exact STORE_NAME instruction.
        def verify_signature(self) -> bool:
            return False

except SyntaxError as exc:
    print(f"  → [Intercepted at Class-Body Execution] {exc}")


print("\n--- Diagnostic 3: Zero-Copy Read-Only Dict View via types.MappingProxyType ---")
internal_routing_table = {"GHY_NODE_01": "10.24.0.1", "BLR_NODE_02": "10.24.0.2"}

# Wrap the mutable dict in CPython's C-level read-only mappingproxy struct (zero data copying)
public_readonly_view = types.MappingProxyType(internal_routing_table)

try:
    # External callers cannot mutate or inject keys through the proxy
    public_readonly_view["ROGUE_NODE"] = "192.168.1.99"
except TypeError as exc:
    print(f"  → [MappingProxy Lock] External write rejected: {exc}")

# Yet internal mutations to the backing dict are reflected live in O(1) with zero copying!
internal_routing_table["DEL_NODE_03"] = "10.24.0.3"
print(f"  → Live Zero-Copy Proxy View  : {dict(public_readonly_view)}")

print(
    "\nStatus: Python fundamentals verified. Silent class-body collisions trapped via PEP 3115 __prepare__ and dictionaries locked via types.MappingProxyType."
)