# Phase 2, Day 45: Actor-Critic Dual-Head Architecture
import torch
import torch.nn as nn
import torch.nn.functional as F

print("--- Booting Actor-Critic RL Architecture ---")

class ActorCritic(nn.Module):
    def __init__(self, state_features, num_actions):
        super().__init__()
        
        # 1. The Shared Foundation
        # Both heads need to understand the environment, so they share the first visual layer.
        self.shared_layer = nn.Sequential(
            nn.Linear(in_features=state_features, out_features=32),
            nn.ReLU()
        )
        
        # 2. The Actor Head (The Decision Maker)
        # Outputs a probability distribution (e.g., 80% chance to jump, 20% chance to duck)
        self.actor_head = nn.Sequential(
            nn.Linear(in_features=32, out_features=num_actions),
            nn.Softmax(dim=-1)
        )
        
        # 3. The Critic Head (The Judge)
        # Outputs a single continuous number representing the "Value" of being in this state
        self.critic_head = nn.Linear(in_features=32, out_features=1)

    def forward(self, state):
        # Pass state through the shared foundation
        base_understanding = self.shared_layer(state)
        
        # Branch out into dual predictions
        action_probabilities = self.actor_head(base_understanding)
        state_value = self.critic_head(base_understanding)
        
        return action_probabilities, state_value

# Initialize the Dual-Head Engine
state_size = 4
action_size = 2  # Action 0 or Action 1
agent = ActorCritic(state_size, action_size)

# Simulating an environmental state tensor
current_state = torch.tensor([[1.0, 0.5, -0.2, 0.1]])

print("Executing Dual-Head State Evaluation...")

# The AI simultaneously decides what to do AND grades its current situation
action_probs, predicted_value = agent(current_state)

print(f"\n--- Network Outputs ---")
print(f"Actor Policy Output: {action_probs.detach().numpy()[0]} (Probability of choosing Action 0 vs 1)")
print(f"Critic Value Score:  {predicted_value.item():.4f} (Predicted safety/reward of this state)")

# The Actor mathematically samples an action based on its probabilities
chosen_action = torch.multinomial(action_probs, num_samples=1).item()
print(f"\nAction Executed based on Probability: {chosen_action}")

print("\nStatus: Actor-Critic shared architecture operational. Ready for Policy Gradient optimization.")