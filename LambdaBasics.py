# Day 9: Lambda Functions - One-line operations for AI pipelines

# Standard function comparison
# def square(x): return x ** 2

# Lambda equivalent
square_lambda = lambda x: x ** 2

# Practical AI use-case: Sorting a list of model configurations by their accuracy score
# The list contains tuples: (Model Name, Accuracy)
models = [("VisionPro", 0.85), ("TextGen", 0.92), ("AudioSynth", 0.78)]

# We use a lambda to tell Python to sort by the second item in the tuple (index 1)
models.sort(key=lambda model: model[1], reverse=True)

print(f"Top Performing Model: {models[0][0]} with {models[0][1]*100}% accuracy")