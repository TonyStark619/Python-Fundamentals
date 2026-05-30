# Day 22: Dictionary Unpacking - Merging AI Configurations

# The default architecture settings
base_config = {
    "model_type": "NeuralNetwork",
    "layers": 5,
    "optimizer": "SGD"
}

# The custom settings for tonight's training run
custom_tuning = {
    "optimizer": "Adam",  # This will overwrite 'SGD'
    "learning_rate": 0.001,
    "batch_size": 64
}

# The ** operator unpacks and merges them. 
# Data on the right automatically overwrites overlapping keys on the left.
final_ai_config = {**base_config, **custom_tuning}

print("--- Initializing Final AI Model Configuration ---")
for key, value in final_ai_config.items():
    print(f"{key}: {value}")