# Day 4: Handling user input and type conversion

# The input() function always reads data as a string
user_age_str = input("Enter your current age: ")

# We must cast it to an integer to do math
age_next_year = int(user_age_str) + 1

print(f"Fast forward! Next year you will be {age_next_year}.")