# Phase 2, Day 58: Sparse Mixture of Experts (MoE) Routing Layer
import torch
import torch.nn as nn
import torch.nn.functional as F

print("--- Booting Mixture of Experts (MoE) Architecture ---")

class MoELayer(nn.Module):
    def __init__(self, embed_dim, num_experts=8, top_k=2):
        super().__init__()
        self.num_experts = num_experts
        self.top_k = top_k
        
        # 1. The Router (The Gating Network)
        # Looks at the incoming embedding and outputs a score for each of the 8 experts
        self.router = nn.Linear(embed_dim, num_experts, bias=False)
        
        # 2. The Experts
        # A list of independent, specialized neural networks
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(embed_dim, embed_dim * 4),
                nn.ReLU(),
                nn.Linear(embed_dim * 4, embed_dim)
            ) for _ in range(num_experts)
        ])

    def forward(self, x):
        batch_size, seq_len, embed_dim = x.size()
        
        # Flatten the sequence to route each word independently
        x_flat = x.view(-1, embed_dim) 
        
        # Step A: The Router scores how well each expert fits this specific word
        router_logits = self.router(x_flat)
        router_probs = F.softmax(router_logits, dim=-1)
        
        # Step B: Top-K Selection
        # We mathematically ban all experts except the top 2 for this specific word
        top_k_probs, top_k_indices = torch.topk(router_probs, self.top_k, dim=-1)
        
        # Normalize the probabilities so the two surviving experts share 100% of the weight
        top_k_probs = top_k_probs / top_k_probs.sum(dim=-1, keepdim=True)
        
        print(f"[Router] Selected Experts {top_k_indices[0].tolist()} with weights {[round(p, 3) for p in top_k_probs[0].tolist()]}")

        # Step C: Execute the Experts (Sparse Computation)
        final_output = torch.zeros_like(x_flat)
        
        # For every word, send it to its assigned top_k experts and blend their answers
        for i in range(self.top_k):
            expert_indices = top_k_indices[:, i] # Which expert won the i-th slot?
            expert_weights = top_k_probs[:, i].unsqueeze(-1) # How much do we trust them?
            
            # In a true production environment, this is highly parallelized.
            # Here, we sequentially simulate the routing for clarity.
            for expert_idx in range(self.num_experts):
                # Find which words were assigned to THIS specific expert
                token_mask = (expert_indices == expert_idx)
                
                if token_mask.any():
                    # Send only those specific words through this expert's network
                    expert_output = self.experts[expert_idx](x_flat[token_mask])
                    
                    # Multiply by the router's trust weight and add to the final output
                    final_output[token_mask] += expert_output * expert_weights[token_mask]
                    
        return final_output.view(batch_size, seq_len, embed_dim)

# Initialize the MoE Layer (Simulating a 256-dim model with 8 experts, routing to top 2)
moe_engine = MoELayer(embed_dim=256, num_experts=8, top_k=2)

# Simulating a sentence of 3 tokens
dummy_sequence = torch.randn(1, 3, 256)

print("Processing Token Sequence through MoE Routing Matrix...\n")
processed_sequence = moe_engine(dummy_sequence)

print("\n--- Network Diagnostics ---")
print(f"Input Matrix Shape:  {list(dummy_sequence.shape)}")
print(f"Output Matrix Shape: {list(processed_sequence.shape)}")
print("Status: Top-K sparse routing successful. Computation strictly limited to active experts.")