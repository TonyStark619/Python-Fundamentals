# Phase 2, Day 56: Beam Search Decoding (Deterministic Generation)
import torch
import torch.nn.functional as F

print("--- Booting Beam Search Generation Engine ---")

# Simulating a vocabulary of 4 words: 0="I", 1="Love", 2="Code", 3="<END>"
vocab_size = 4
beam_width = 2

# A mock neural network that predicts the next word's logits based on the sequence
def mock_model_predict(sequence):
    # In production, this runs the sequence through the Transformer Decoder.
    # Here, we return random logits to simulate AI predictions.
    return torch.randn(1, vocab_size)

# Initial state: We start with a blank sequence and a log-probability score of 0.0 (100%)
# Format: (Current Log Probability, Sequence of Token IDs)
beams = [(0.0, [0])]  # Assuming 0 is our starting token

max_sequence_length = 3
print(f"Executing Beam Search (Beam Width = {beam_width})...")

for step in range(max_sequence_length):
    all_candidates = list()
    
    # 1. Expand ALL currently surviving beams
    for current_score, current_seq in beams:
        logits = mock_model_predict(current_seq)
        
        # We use Log-Softmax because adding logs is mathematically safer than multiplying tiny percentages
        log_probabilities = F.log_softmax(logits, dim=-1)[0]
        
        # 2. Generate future branch candidates for this specific beam
        for word_id in range(vocab_size):
            candidate_score = current_score + log_probabilities[word_id].item()
            candidate_seq = current_seq + [word_id]
            all_candidates.append((candidate_score, candidate_seq))
            
    # 3. THE PRUNE (The core of Beam Search)
    # Sort all futures by their cumulative probability score (Highest first)
    ordered_candidates = sorted(all_candidates, key=lambda x: x[0], reverse=True)
    
    # Keep strictly the top 'B' futures and mathematically kill the rest
    beams = ordered_candidates[:beam_width]
    
    print(f"\nStep {step + 1} - Top {beam_width} surviving beams:")
    for rank, (score, seq) in enumerate(beams):
        print(f"  Rank {rank+1}: Sequence {seq} | Cumulative Log-Prob: {score:.4f}")

print("\n--- Output Diagnostics ---")
best_score, best_sequence = beams[0]
print(f"Optimal Generated Sequence: {best_sequence}")
print("Status: O(B * V) Beam expansion and pruning complete. Optimal sequence isolated.")