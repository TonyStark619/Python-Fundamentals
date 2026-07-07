# Phase 2, Day 29: Autoregressive Text Generation
import torch
import torch.nn as nn

print("--- Booting LLM Generation Protocol ---")

class DummyLLM(nn.Module):
    def __init__(self, vocab_size):
        super().__init__()
        self.vocab_size = vocab_size
        # Simulating a massive Transformer Brain that outputs probabilities for every word
        # In reality, this would be the TransformerBlock you built yesterday
        self.brain = nn.Linear(1, vocab_size)

    def forward(self, current_sequence):
        # We simulate the AI looking at the sequence and generating raw scores (logits) for the next word
        # (Using a dummy calculation for architectural demonstration)
        last_word = current_sequence[:, -1].float().unsqueeze(1)
        return self.brain(last_word)

# Initialize the architecture (Dictionary Size: 5000 words)
vocab_size = 5000
ai_model = DummyLLM(vocab_size)

# Let's say our starting prompt is the word ID [42] ("The")
current_sequence = torch.tensor([[42]])
max_length = 8 # We want the AI to write a sentence of 8 words

print(f"Initial Prompt ID: {current_sequence.tolist()[0]}\n")
print("Executing Autoregressive Loop...")

# The exact loop used by ChatGPT to generate text
for step in range(max_length - 1):
    # 1. Pass the current sentence into the brain
    logits = ai_model(current_sequence)
    
    # 2. Find the index of the highest probability word (Greedy Search)
    next_word_id = torch.argmax(logits, dim=-1)
    
    # 3. Append the new word to our sentence
    current_sequence = torch.cat([current_sequence, next_word_id], dim=1)
    
    print(f"Step {step + 1} | Generated Word ID: {next_word_id.item():4d} | Current Sequence: {current_sequence.tolist()[0]}")

print("\n--- Generation Complete ---")
print("Status: Context successfully expanded. Ready for string decoding.")