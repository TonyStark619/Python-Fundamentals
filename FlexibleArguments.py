# Day 21: *args and **kwargs - Flexible AI Model Initialization

def initialize_ai_model(model_name, *args, **kwargs):
    """Simulates initializing an AI model with variable configurations."""
    print(f"--- Booting {model_name} ---")
    
    # *args packs extra unnamed arguments into a tuple
    if args:
        print(f"Loaded Core Modules: {args}")
        
    # **kwargs packs extra named arguments into a dictionary
    if kwargs:
        print("Applying Hyperparameters:")
        for key, value in kwargs.items():
            print(f"  -> {key}: {value}")

# Instantiating the model like a senior AI architect
initialize_ai_model(
    "VisionPro_v3", 
    "EdgeDetection", "DepthSensor", # Unnamed args go to *args
    learning_rate=0.001, epochs=500, optimizer="Adam" # Named args go to **kwargs
)