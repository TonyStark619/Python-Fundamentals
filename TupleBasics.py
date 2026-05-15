# Day 7: Tuples - Protecting your data

# Tuples are created with parentheses () instead of brackets []
model_dimensions = (1920, 1080)

print(f"Image Width: {model_dimensions[0]}")
print(f"Image Height: {model_dimensions[1]}")

# UNCOMMENTING THE LINE BELOW WILL CAUSE AN ERROR
# model_dimensions[0] = 1280 

print("Attempting to change a tuple will crash the program. It is immutable and safe!")