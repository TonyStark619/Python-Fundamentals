# Day 10: Exception Handling - Preventing pipeline crashes

def process_data(data_string):
    """Simulates cleaning a single row of AI dataset"""
    try:
        # Attempting to convert a string to an integer
        value = int(data_string)
        print(f"Success! Processed value: {value}")
    except ValueError:
        # This block catches the error so the whole program doesn't die
        print(f"Error: Data '{data_string}' is corrupted. Skipping to next item.")

# Simulating a dirty dataset
print("--- Starting Pipeline ---")
process_data("1024")  # Clean data
process_data("N/A")   # Dirty data (This would normally crash the program)
process_data("2048")  # Clean data