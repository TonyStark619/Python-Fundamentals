# Phase 2, Day 49: KV Cache for Accelerated LLM Generation
import torch
import torch.nn as nn

print("--- Booting LLM KV Cache Engine ---")

class FastAttentionWithCache(nn.Module):
    def __init__(self, embed_dim):
        super().__init__()
        # In a real transformer, these generate the Query, Key, and Value matrices
        self.q_proj = nn.Linear(embed_dim, embed_dim, bias=False)
        self.k_proj = nn.Linear(embed_dim, embed_dim, bias=False)
        self.v_proj = nn.Linear(embed_dim, embed_dim, bias=False)
        self.embed_dim = embed_dim

    def forward(self, new_token, past_key_cache=None, past_value_cache=None):
        # 1. Calculate Q, K, V for just the ONE new token
        query = self.q_proj(new_token)
        new_key = self.k_proj(new_token)
        new_value = self.v_proj(new_token)

        # 2. Update the Cache
        if past_key_cache is not None and past_value_cache is not None:
            # Concatenate (glue) the old memory with the new token's memory
            keys = torch.cat([past_key_cache, new_key], dim=1)
            values = torch.cat([past_value_cache, new_value], dim=1)
            print(f"[Engine] Cache hit! Expanding memory sequence length to {keys.shape[1]}")
        else:
            # First token being generated, start the cache
            keys = new_key
            values = new_value
            print("[Engine] Cold start. Initializing fresh KV Cache.")

        # 3. Calculate Attention using the newly updated cache
        # We only compute Q for the single token, multiplied by the entire Key memory
        attention_scores = torch.matmul(query, keys.transpose(-2, -1)) / (self.embed_dim ** 0.5)
        attention_weights = torch.softmax(attention_scores, dim=-1)
        
        # Multiply by the Value memory to get the final context
        output = torch.matmul(attention_weights, values)

        # Return the output AND the updated cache for the next cycle
        return output, keys, values

# Simulating deployment
embed_size = 16
inference_engine = FastAttentionWithCache(embed_size)

print("Starting Autoregressive Generation Loop...\n")

# Token 1 (The prompt)
token_1 = torch.randn(1, 1, embed_size)
print("Step 1: Generating Token 1...")
out_1, k_cache, v_cache = inference_engine(token_1)

# Token 2 (Generated based strictly on Token 1)
# We pass in the cache so it doesn't recalculate Token 1
token_2 = torch.randn(1, 1, embed_size)
print("\nStep 2: Generating Token 2...")
out_2, k_cache, v_cache = inference_engine(token_2, past_key_cache=k_cache, past_value_cache=v_cache)

# Token 3
token_3 = torch.randn(1, 1, embed_size)
print("\nStep 3: Generating Token 3...")
out_3, k_cache, v_cache = inference_engine(token_3, past_key_cache=k_cache, past_value_cache=v_cache)

print("\n--- Diagnostics ---")
print(f"Final Cache Memory Footprint: {list(k_cache.shape)} (Holding 3 tokens)")
print("Status: KV Caching operational. O(N^2) redundancy eliminated for real-time text streaming.")