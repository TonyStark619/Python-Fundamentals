# Phase 2, Day 46: Proximal Policy Optimization (PPO) - The OpenAI Standard
import torch

print("--- Booting PPO Clipped Objective Engine ---")

# Simulating data from our Actor-Critic model
# Epsilon is the safety boundary. The AI cannot change its policy by more than 20% per step.
epsilon_clip = 0.2

# 1. The Actor's Probabilities
# How likely the OLD brain thought this action was vs how likely the NEW brain thinks it is.
old_policy_probs = torch.tensor([0.40, 0.60, 0.30]) 
new_policy_probs = torch.tensor([0.45, 0.85, 0.25]) 

# 2. The Critic's Judgment (Advantages)
# Positive means the action was better than expected. Negative means it was worse.
advantages = torch.tensor([1.0, 2.0, -1.0])

print("Calculating Policy Ratio (New / Old)...")
# Calculate the ratio. If ratio > 1, the new policy is taking this action MORE often.
ratios = new_policy_probs / old_policy_probs
for i, ratio in enumerate(ratios):
    print(f"  Action {i+1} Ratio: {ratio.item():.2f}")

# 3. The PPO Math (The Clip)
# Calculate the raw, unconstrained mathematical update
surrogate_1 = ratios * advantages

# Calculate the strictly constrained (clipped) update
# torch.clamp forces the ratio to stay between 0.8 and 1.2
clipped_ratios = torch.clamp(ratios, 1.0 - epsilon_clip, 1.0 + epsilon_clip)
surrogate_2 = clipped_ratios * advantages

# The PPO rule: Take the MINIMUM of the unclipped and clipped versions.
# This ensures we never take a massive, dangerous update step.
ppo_loss_array = torch.min(surrogate_1, surrogate_2)

# We want to MAXIMIZE the reward, but PyTorch optimizers always MINIMIZE loss.
# So, we multiply by -1 to flip the math, and take the mean to get a single loss number.
final_ppo_loss = -ppo_loss_array.mean()

print(f"\n--- Optimization Diagnostics ---")
print(f"Unclipped Raw Updates: {surrogate_1.tolist()}")
print(f"Clipped Safe Updates:  {surrogate_2.tolist()}")
print(f"Final Step Loss (Gradient): {final_ppo_loss.item():.4f}")
print("\nStatus: PPO Clip operational. Policy update stabilized. Neural collapse prevented.")