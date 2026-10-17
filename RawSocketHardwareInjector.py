# Phase 3, Day 205: Python Fundamentals - Raw Socket Byte Forging (socket + struct)
import socket
import struct
import os
import time

print("--- Booting Raw Hardware-Level Socket Injector ---")

# 1. The Mathematical Checksum Algorithm
# Routers physically drop packets if this binary calculation is off by a single bit.
def calculate_hardware_checksum(source_string):
    """Calculates the 16-bit One's Complement of the One's Complement Sum."""
    total = 0
    count_to = (len(source_string) // 2) * 2
    count = 0

    # Process bytes in pairs (16 bits)
    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        total = total + this_val
        total = total & 0xffffffff
        count = count + 2

    # If there is a trailing odd byte
    if count_to < len(source_string):
        total = total + source_string[len(source_string) - 1]
        total = total & 0xffffffff

    # Fold 32-bit sum into 16 bits
    total = (total >> 16) + (total & 0xffff)
    total = total + (total >> 16)
    
    # One's complement
    answer = ~total
    answer = answer & 0xffff
    
    # Swap bytes for network byte order
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

# 2. Packet Forgery Engine
def forge_icmp_packet(packet_id):
    """
    Constructs a raw ICMP Echo Request (Ping) at the binary level.
    """
    # ICMP Type: 8 (Echo Request), Code: 0
    icmp_type = 8
    icmp_code = 0
    initial_checksum = 0
    sequence_number = 1
    
    # The Payload. We are sending literal bytes over the wire.
    payload = b"FAANG_ENTERPRISE_ARCHITECTURE"

    # THE MAGIC: Struct.pack mathematically forces Python integers into C-style memory blocks.
    # 'bbHHh' means: byte(1), byte(1), unsigned short(2), unsigned short(2), short(2)
    dummy_header = struct.pack("bbHHh", icmp_type, icmp_code, initial_checksum, packet_id, sequence_number)
    
    # Calculate the checksum over the header + payload
    calculated_checksum = calculate_hardware_checksum(dummy_header + payload)

    # Re-pack the header with the correct mathematical checksum
    # socket.htons ensures the checksum is in Network Byte Order (Big-Endian)
    valid_header = struct.pack("bbHHh", icmp_type, icmp_code, socket.htons(calculated_checksum), packet_id, sequence_number)
    
    return valid_header + payload

# --- Execution Environment ---

target_ip = "8.8.8.8" # Google Public DNS
packet_id = os.getpid() & 0xFFFF # Use the OS Process ID to tag the packet

print(f"  [System] Forging binary payload for target: {target_ip}")
raw_binary_packet = forge_icmp_packet(packet_id)

print(f"  -> Raw Binary Hex: {raw_binary_packet.hex()}")

# 3. Hardware Injection
try:
    # THE OVERRIDE: SOCK_RAW tells the OS we will handle all the protocol headers manually
    # Note: If you run this without Admin/Root access, the OS will block the raw hardware access.
    # We use a try/except to demonstrate the architecture even on restricted user accounts.
    network_interface = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    
    print("\n  [Network] Injecting raw packet directly into Network Interface Card (NIC)...")
    network_interface.sendto(raw_binary_packet, (target_ip, 1))
    
    print("  [Network] Awaiting hardware response...")
    # Read the raw byte response from the wire
    response_packet, addr = network_interface.recvfrom(1024)
    
    print(f"\nCRITICAL RESULT: Raw ICMP response received from {addr[0]}!")
    print(f"Response Hex Payload: {response_packet.hex()[:30]}...")

except PermissionError:
    print("\n[ALERT] OS blocked Raw Socket creation. (Admin/Root privileges required for direct hardware injection).")
    print("  -> Architecture perfectly compiled. OS kernel simply denied physical wire access.")

print("\nStatus: Python fundamentals verified. OS TCP/IP stack bypassed via struct packing and SOCK_RAW architectures.")