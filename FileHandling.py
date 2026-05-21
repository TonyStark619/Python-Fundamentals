# Day 13: File Handling - Logging AI Training Data

log_file = "model_logs.txt"

# 1. Writing to a file ("w" mode overwrites the file)
with open(log_file, "w") as file:
    file.write("AI Model: VisionPro_v1\n")
    file.write("Epoch 1: Accuracy 0.85\n")
    file.write("Epoch 2: Accuracy 0.89\n")

print("Logs written successfully.\n")

# 2. Reading from the file ("r" mode reads the file)
print("--- Reading Training Logs ---")
with open(log_file, "r") as file:
    content = file.read()
    print(content)