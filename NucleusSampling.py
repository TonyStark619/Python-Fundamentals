# Phase 2, Day 55: Top-p (Nucleus) Dynamic Sampling
import torch
import torch.nn.functional as F

print("--- Booting LLM Nucleus Sampling Engine ---")

# Simulating raw output logits for 7 vocabulary words
raw_logits = torch.tensor([[ -1.5,  2.0,  5.5,  0.5,  4.0, -0.5,  1.2 ]])

# Step 1: Convert raw logits to percentages
probabilities = F.softmax(raw_logits, dim=-1)
print(f"Initial Probabilities: {[f'{p.item()*100:.1f}%' for p in probabilities[0]]}")

# Step 2: Sort the probabilities in descending order (highest first)
sorted_probs, sorted_indices = torch.sort(probabilities, descending=True)

# Step 3: Calculate the Cumulative Sum (The "Mass")
cumulative_probs = torch.cumsum(sorted_probs, dim=-1)
print(f"Cumulative Mass Array: {[f'{p.item()*100:.1f}%' for p in cumulative_probs[0]]}")

# --- THE NUCLEUS THRESHOLD ---
# We only want to keep the words that make up the top 85% of the probability mass
top_p_threshold = 0.85
print(f"\nApplying Top-p Threshold (p={top_p_threshold})...")

# Create a boolean mask of words to mathematically ban
# We shift the mask right by 1 to ensure we ALWAYS keep at least the #1 most likely word
sorted_indices_to_remove = cumulative_probs > top_p_threshold
sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
sorted_indices_to_remove[..., 0] = 0

# Scatter the mask back to the original index order
indices_to_remove = sorted_indices_to_remove.scatter(1, sorted_indices, sorted_indices_to_remove)

# Step 4: Ban the weak words by setting their logits to negative infinity
filtered_logits = raw_logits.masked_fill(indices_to_remove, float('-inf'))

# Step 5: Recalculate the probabilities among ONLY the surviving words
final_probabilities = F.softmax(filtered_logits, dim=-1)
print(f"Final Filtered Probabilities: {[f'{p.item()*100:.1f}%' for p in final_probabilities[0]]}")

# Roll the dice based on the dynamic probability pool
sampled_token_index = torch.multinomial(final_probabilities, num_samples=1).item()

print("\n--- Output Diagnostics ---")
print(f"Selected Token ID: {sampled_token_index}")
print("Status: Top-p cumulative mass filter applied. Dynamic vocabulary scaling successful.")