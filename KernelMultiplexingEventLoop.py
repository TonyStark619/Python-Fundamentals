# Phase 3, Day 204: Python Fundamentals - OS Kernel I/O Multiplexing (selectors)
import selectors
import socket
import urllib.parse

print("--- Booting Custom OS-Level Event Loop ---")

# 1. Access the underlying Hardware/OS Multiplexer (epoll/kqueue)
kernel_selector = selectors.DefaultSelector()

# Track how many active requests we have so we know when to shut down
active_connections = 0

def construct_http_request(host, path):
    """Builds a raw HTTP GET request string."""
    return f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n".encode('utf-8')

def dispatch_async_request(url):
    """Initiates a non-blocking network connection and registers it with the OS."""
    global active_connections
    
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.netloc
    path = parsed_url.path if parsed_url.path else '/'
    
    # Create a raw TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # THE MAGIC: Make the socket non-blocking. 
    # Python will NOT wait for the connection to establish. It executes instantly.
    client_socket.setblocking(False)
    
    try:
        client_socket.connect((host, 80))
    except BlockingIOError:
        # This is expected. The OS is establishing the connection in the background.
        pass
        
    print(f"  [Network] Socket dispatched for {host}. Registering OS hook...")
    
    # Create a payload of the data we need to send once the OS says the socket is ready
    request_payload = construct_http_request(host, path)
    
    # Register the socket with the OS Kernel. 
    # We ask the OS to wake us up when this socket is writable (ready to send data)
    kernel_selector.register(
        client_socket, 
        selectors.EVENT_WRITE, 
        data={'state': 'connecting', 'payload': request_payload, 'host': host}
    )
    active_connections += 1

def handle_os_event(key, mask):
    """Callback executed when the OS wakes our thread up."""
    global active_connections
    client_socket = key.fileobj
    connection_data = key.data
    
    if mask & selectors.EVENT_WRITE:
        # The OS says the socket is connected. Send the HTTP request.
        print(f"    -> [Kernel Hook] {connection_data['host']} connected. Blasting payload...")
        client_socket.sendall(connection_data['payload'])
        
        # We sent the data. Now we ask the OS to wake us up when the server replies (Readable)
        kernel_selector.modify(client_socket, selectors.EVENT_READ, data=connection_data)
        
    elif mask & selectors.EVENT_READ:
        # The OS says the server sent data back. Read it.
        print(f"    -> [Kernel Hook] {connection_data['host']} responded. Reading buffer...")
        response_chunk = client_socket.recv(4096)
        
        if response_chunk:
            pass # In a real app, we would append this to a buffer
        else:
            # An empty response means the server closed the connection. We are done.
            print(f"  [Success] Transaction complete for {connection_data['host']}.")
            kernel_selector.unregister(client_socket)
            client_socket.close()
            active_connections -= 1

# --- Execution Environment ---

print("\n[System] Dispatching concurrent requests. Single thread executing...\n")
# We dispatch three requests sequentially. Because they are non-blocking, they execute in microseconds.
dispatch_async_request("http://www.example.com")
dispatch_async_request("http://www.httpbin.org")
dispatch_async_request("http://www.w3.org")

print("\n[System] Entering Infinite Event Loop (Sleeping until OS hardware interrupts)...\n")

# THE EVENT LOOP: The absolute core of asynchronous programming
while active_connections > 0:
    # Python puts the thread to sleep here. Zero CPU usage.
    # It wakes up the millisecond the OS kernel triggers an event.
    events = kernel_selector.select()
    
    for key, mask in events:
        handle_os_event(key, mask)

print("\nStatus: Python fundamentals verified. Single-threaded async Event Loop mathematically engineered via OS kernel multiplexing.")