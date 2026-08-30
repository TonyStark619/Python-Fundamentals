# Python: List Operations & Dynamic Exception Handling
def process_data():
    # Dynamic list (resizes automatically)
    data_stream = [10, 20, 0, 40]
    
    print("--- Python Execution ---")
    
    # Intentionally pushing out of bounds to trigger an exception
    for i in range(len(data_stream) + 1):
        try:
            result = 100 // data_stream[i]
            print(f"Processed: {result}")
        except ZeroDivisionError:
            print("Error: Cannot divide by zero.")
        except IndexError:
            print("Error: List index out of range.")

if __name__ == "__main__":
    process_data()