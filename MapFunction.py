# Day 17: The map() function - Data transformation at scale

# Simulating a raw dataset (e.g., temperatures in Celsius)
celsius_data = [0, 20, 25, 30, 100]

# Using map() and a lambda function to convert the entire list to Fahrenheit instantly
fahrenheit_data = list(map(lambda c: (c * 9/5) + 32, celsius_data))

print("--- AI Data Preprocessing ---")
print(f"Raw Data (Celsius):       {celsius_data}")
print(f"Transformed (Fahrenheit): {fahrenheit_data}")