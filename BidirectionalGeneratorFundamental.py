# Phase 3, Day 62: Python Fundamentals - Bidirectional Generators (Stateful Coroutines)
print("--- Booting Python Fundamental Stateful Coroutine ---")

def anomaly_detector():
    """
    A bidirectional generator that maintains internal state.
    It yields the current moving average OUT, and accepts new sensor readings IN.
    """
    total = 0
    count = 0
    current_average = 0.0
    
    print("  [Coroutine] Internal memory initialized. Awaiting data stream...")
    
    while True:
        # THE MAGIC: yield pauses the loop and spits out current_average.
        # When .send() is called, it injects the new value directly into new_reading.
        new_reading = yield current_average
        
        # If the main program explicitly sends None, we do nothing and wait for the next loop
        if new_reading is None:
            continue
            
        print(f"  [Coroutine] Received new data point: {new_reading}")
        
        # Update the persistent internal state
        total += new_reading
        count += 1
        current_average = total / count
        
        # Anomaly detection logic based on historical state
        if new_reading > (current_average * 2) and count > 2:
            print(f"  [Coroutine] CRITICAL ALERT: Spike detected! ({new_reading} is > 200% of avg {current_average:.1f})")

# --- Execution Environment ---
print("\n[System] Spawning isolated anomaly detection coroutine...")

# 1. Instantiate the generator
stream_analyzer = anomaly_detector()

# 2. "Prime" the generator. 
# We MUST call next() once to advance the code execution up to the very first 'yield' statement.
next(stream_analyzer) 

print("\n--- Initiating Live Data Telemetry Stream ---")
# 3. Inject data dynamically using .send()
sensor_data = [10, 12, 11, 45, 14, 15]

for reading in sensor_data:
    # Send the reading IN, and instantly get the updated average OUT
    updated_avg = stream_analyzer.send(reading)
    print(f"[Main Thread] Current Moving Average: {updated_avg:.1f}\n")

# 4. Safely terminate the coroutine to free memory
stream_analyzer.close()

print("Status: Python fundamentals verified. Bidirectional data streams successfully maintained isolated state logic.")