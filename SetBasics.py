# Day 6: Sets - Removing duplicates instantly

# A list with duplicate data entries
raw_data = ["apple", "banana", "apple", "cherry", "banana"]
print(f"Raw data: {raw_data}")

# Converting the list to a Set automatically strips out duplicates
clean_data = set(raw_data)
print(f"Cleaned data (Set): {clean_data}")

# Sets are unordered, so the output order may change!