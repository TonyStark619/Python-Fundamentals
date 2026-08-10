# Phase 2, Day 68: Byte-Pair Encoding (BPE) Tokenization
import collections

print("--- Booting BPE Tokenizer Engine ---")

def get_pair_frequencies(vocab):
    """Scans the vocabulary and counts how often adjacent characters appear together."""
    pairs = collections.defaultdict(int)
    for word, frequency in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            # Form a tuple of the adjacent pair
            pair = (symbols[i], symbols[i + 1])
            pairs[pair] += frequency
    return pairs

def merge_most_frequent_pair(pair, vocab):
    """Fuses the highest frequency pair into a single new token across the entire vocabulary."""
    new_vocab = {}
    # Create the regex-style replacement strings
    bigram = " ".join(pair)
    replacement = "".join(pair)
    
    for word, frequency in vocab.items():
        # Replace the separated characters with the fused token
        new_word = word.replace(bigram, replacement)
        new_vocab[new_word] = frequency
        
    return new_vocab

# --- Simulation Environment ---
# We represent words as space-separated characters initially, ending with a special </w> token.
# The numbers represent how many times that word appeared in our training text.
corpus_vocab = {
    "l o w </w>": 5,
    "l o w e s t </w>": 2,
    "n e w e r </w>": 6,
    "w i d e r </w>": 3,
    "n e w </w>": 2
}

print("Ingesting Training Corpus...")
num_merges = 5

for i in range(num_merges):
    # 1. Map the frequencies of all adjacent pairs
    pair_freqs = get_pair_frequencies(corpus_vocab)
    
    if not pair_freqs:
        break
        
    # 2. Find the absolute most frequent pair in the dataset
    best_pair = max(pair_freqs, key=pair_freqs.get)
    
    # 3. Fuse them into a new subword token
    corpus_vocab = merge_most_frequent_pair(best_pair, corpus_vocab)
    
    print(f"\nMerge Step {i + 1}: Fusing '{best_pair[0]}' and '{best_pair[1]}' -> '{''.join(best_pair)}'")
    print(f"Current Vocabulary State: {list(corpus_vocab.keys())[:2]}...")

print("\n--- Tokenization Diagnostics ---")
print("Status: Subword chunking complete. Vocabulary dynamically optimized for LLM embedding layer.")