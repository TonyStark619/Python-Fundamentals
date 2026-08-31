# Python: List Comprehension for Filtering and Mapping
def process_data():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    
    # Filter even numbers and square them in one line
    squared_evens = [n * n for n in numbers if n % 2 == 0]
    
    print(f"Python Processed: {squared_evens}")
    # Output: [4, 16, 36, 64]

if __name__ == "__main__":
    process_data()