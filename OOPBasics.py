# Day 14: Object-Oriented Programming - The blueprint for AI Models

class AIModel:
    def __init__(self, name, version):
        self.name = name
        self.version = version

    def train(self):
        print(f"Training {self.name} (Version {self.version}) initialized...")
        print("Loss decreasing... Weights optimized... Done.")

# Instantiating the object
vision_model = AIModel("VisionPro", "v2.0")
vision_model.train()

print("14-Day Reset Protocol: COMPLETE.")