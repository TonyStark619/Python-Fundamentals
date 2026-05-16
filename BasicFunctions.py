# Day 8: Defining Reusable Functions

def greet_developer(name, role):
    """A simple function to greet the user."""
    print(f"Welcome back, {name}.")
    print(f"Your target role is: {role}. Let's build.")

# Calling the function with arguments
greet_developer("AI Architect", "50 LPA Big Tech")

def calculate_ai_salary(base, bonus):
    """Returns the total compensation."""
    return base + bonus

# Capturing the return value
total_comp = calculate_ai_salary(35, 15)
print(f"Target Total Compensation: {total_comp} LPA")