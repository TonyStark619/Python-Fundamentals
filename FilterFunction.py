# Day 18: The filter() function - Data cleaning at scale

# Simulating a raw AI dataset with some invalid (negative) values or noise
sensor_readings = [12, -5, 34, 8, -99, 45, 0, 23]

# Using filter() and lambda to keep only the positive, valid readings
clean_data = list(filter(lambda x: x > 0, sensor_readings))

print("--- AI Data Pipeline: Noise Reduction ---")
print(f"Raw Sensor Data: {sensor_readings}")
print(f"Cleaned Data:    {clean_data}")