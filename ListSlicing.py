# Day 5: Master the Art of Slicing
numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Get the first 5 elements
first_half = numbers[:5]

# Get elements from index 5 to the end
second_half = numbers[5:]

# The "Pro" Move: Get every second number (Stepping)
evens = numbers[::2]

print(f"Original: {numbers}")
print(f"First Half: {first_half}")
print(f"Every Second Number: {evens}")