# Phase 2, Day 54: LLM Decoding (Temperature & Top-K Sampling)
import torch
import torch.nn.functional as F

print("--- Booting LLM Generation Controller ---")

# Simulating raw neural network output (Logits) for the next word in a sentence.
# Let's say our vocabulary only has 7 words.
# Word Indices: 0="Apple", 1="Banana", 2="Cat", 3="Dog", 4="Elephant", 5="Fox", 6="Giraffe"
raw_logits = torch.tensor([[ -1.5,  2.0,  5.5,  0.5,  4.0, -0.5,  1.2 ]])
vocab_size = raw_logits.size(-1)

print(f"Raw Model Logits: {raw_logits.tolist()[0]}")

# --- 1. TEMPERATURE SCALING ---
# Temp < 1.0 = More confident/robotic. Temp > 1.0 = More creative/random. Temp = 1.0 = Default.
temperature = 0.8
print(f"\nApplying Temperature Scaling (T={temperature})...")

scaled_logits = raw_logits / temperature

# --- 2. TOP-K FILTERING ---
# We only want the AI to choose between the Top 3 most logical words. 
# Everything else gets mathematically banned.
top_k_limit = 3
print(f"Applying Top-K Filter (K={top_k_limit})...")

# Find the values and indices of the top K elements
top_k_values, top_k_indices = torch.topk(scaled_logits, top_k_limit, dim=-1)

# Create a mask of negative infinities (banning all words)
filtered_logits = torch.full_like(scaled_logits, float('-inf'))

# Scatter the valid top-k values back into the exact slots they belong in
filtered_logits.scatter_(dim=-1, index=top_k_indices, src=top_k_values)

# --- 3. PROBABILITY CONVERSION & SAMPLING ---
# Convert the filtered logits into actual percentages using Softmax
final_probabilities = F.softmax(filtered_logits, dim=-1)
print(f"\nFinal Probability Distribution: {[f'{p.item()*100:.1f}%' for p in final_probabilities[0]]}")

# Roll the dice based on the calculated probabilities
# torch.multinomial acts as a weighted roulette wheel
sampled_token_index = torch.multinomial(final_probabilities, num_samples=1).item()

print("\n--- Output Diagnostics ---")
print(f"Selected Token ID: {sampled_token_index}")
print("Status: Top-K extraction and Temperature manipulation successful. Token generated safely.")