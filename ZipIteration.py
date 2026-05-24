# Day 16: The zip() function - Parallel iteration for datasets

# Simulating AI feature inputs and their corresponding labels
features = ["Pixels", "Audio Waves", "Text Tokens"]
labels = ["Computer Vision", "Speech Recognition", "NLP"]

print("--- AI Pipeline Mapping ---")
# zip() pairs the elements up automatically
for x, y in zip(features, labels):
    print(f"Input: {x} -> Target Domain: {y}")