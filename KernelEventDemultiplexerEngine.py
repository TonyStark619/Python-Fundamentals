# Phase 3, Master Day 236: Python Fundamentals - OS Kernel I/O Demultiplexing (selectors + socketpair)
import selectors
import socket
from dataclasses import dataclass
from typing import Dict, Tuple

print("--- Booting CPython OS-Kernel Non-Blocking I/O Reactor Engine ---")


@dataclass
class ChannelContext:
    """Metadata payload attached directly to the OS kernel selector key."""
    channel_name: str
    bytes_received: int = 0
    frames_processed: int = 0


def read_ready_channel(
    selector: selectors.BaseSelector,
    rx_socket: socket.socket,
    ctx: ChannelContext,
) -> None:
    """
    Non-blocking read callback invoked ONLY when the OS kernel signals EVENT_READ readiness.
    """
    try:
        chunk = rx_socket.recv(4096)
    except BlockingIOError:
        # Kernel buffer transiently empty on a non-blocking socket; return control immediately
        return

    if chunk:
        ctx.bytes_received += len(chunk)
        ctx.frames_processed += 1
        print(
            f"    [Kernel Wakeup -> {ctx.channel_name}] Drained {len(chunk)} bytes: "
            f"{chunk.decode('utf-8')!r}"
        )
    else:
        # Receiving b"" (0 bytes) on a readable socket signals clean TCP FIN / EOF from peer
        print(
            f"    [Kernel EOF    -> {ctx.channel_name}] Peer closed stream. "
            f"Total: {ctx.bytes_received} bytes across {ctx.frames_processed} wakes. Unregistering FD."
        )
        selector.unregister(rx_socket)
        rx_socket.close()


# --- Execution Environment ---

# Automatically binds to EpollSelector (Linux), KqueueSelector (macOS), or SelectSelector (Windows)
reactor = selectors.DefaultSelector()
print(f"  [OS Kernel Hook] Bound Native Selector Backend : {type(reactor).__name__}")

# Spawn 3 independent full-duplex non-blocking socket pairs in memory
channels: Dict[str, Tuple[socket.socket, socket.socket]] = {}
for name in ("SHARD_ALPHA", "SHARD_BETA", "SHARD_GAMMA"):
    tx_sock, rx_sock = socket.socketpair()
    tx_sock.setblocking(False)
    rx_sock.setblocking(False)

    # Register ONLY the receiving end with the kernel reactor for READ readiness
    reactor.register(rx_sock, selectors.EVENT_READ, data=ChannelContext(channel_name=name))
    channels[name] = (tx_sock, rx_sock)

print(f"  [OS Kernel Hook] Registered {len(reactor.get_map())} non-blocking FDs on a SINGLE OS thread.\n")

try:
    print("--- Wave 1: Selective Kernel Wakeup (Alpha & Gamma active; Beta idle) ---")
    channels["SHARD_GAMMA"][0].sendall(b"TELEMETRY::TEMP=41C::LOAD=78%")
    channels["SHARD_ALPHA"][0].sendall(b"LEDGER::COMMIT_HASH=9F4A2C")

    # Single kernel syscall returns ONLY ready descriptors (SHARD_BETA consumes 0 CPU cycles!)
    ready_events = reactor.select(timeout=0.5)
    print(f"  → Kernel returned {len(ready_events)} ready descriptors out of {len(reactor.get_map())} monitored:")
    for key, _mask in ready_events:
        read_ready_channel(reactor, key.fileobj, key.data)

    print("\n--- Wave 2: Interleaved Burst + Clean EOF Teardown Loop ---")
    channels["SHARD_BETA"][0].sendall(b"HEARTBEAT::QUORUM_SYNC_OK")
    channels["SHARD_ALPHA"][0].sendall(b"LEDGER::FINALIZE_EPOCH_236")

    # Close all writer sockets to transmit OS-level EOF (FIN) signals
    for tx_sock, _ in channels.values():
        tx_sock.close()

    # Pure Reactor Event Loop: runs until every registered FD has drained and closed cleanly
    tick = 0
    while reactor.get_map():
        tick += 1
        events = reactor.select(timeout=0.5)
        print(f"  [Reactor Tick #{tick}] Kernel signaled {len(events)} descriptor(s):")
        for key, _mask in events:
            read_ready_channel(reactor, key.fileobj, key.data)

finally:
    reactor.close()

print(
    "\nStatus: Python fundamentals verified. Multi-channel non-blocking I/O multiplexed on a single thread via native OS kernel selectors."
)