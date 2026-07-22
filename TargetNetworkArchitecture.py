# Phase 2, Day 44: RL Target Network (Double Brain Architecture)
import torch
import torch.nn as nn

print("--- Booting Dual-Network RL Architecture ---")

# 1. The Core Neural Architecture
class QNetwork(nn.Module):
    def __init__(self, state_features, num_actions):
        super().__init__()
        self.brain = nn.Sequential(
            nn.Linear(in_features=state_features, out_features=24),
            nn.ReLU(),
            nn.Linear(in_features=24, out_features=num_actions)
        )

    def forward(self, state):
        return self.brain(state)

# 2. Instantiate the TWO Brains
state_size = 4
action_size = 2

policy_net = QNetwork(state_size, action_size) # The active, learning brain
target_net = QNetwork(state_size, action_size) # The frozen, calculating brain

# 3. Synchronize them perfectly at Step 0
# We copy the exact mathematical weights from the active brain to the frozen brain
target_net.load_state_dict(policy_net.state_dict())
target_net.eval() # Tell PyTorch this network is frozen (no gradients/learning)

print("Status: Policy Network and Target Network initialized and synchronized.")

# Simulating a training step
dummy_state = torch.tensor([[1.0, 0.5, -0.2, 0.1]])
dummy_next_state = torch.tensor([[0.9, 0.6, -0.1, 0.0]])

print("\nExecuting Bellman Target Calculation...")

# The active brain evaluates what to do RIGHT NOW
current_predictions = policy_net(dummy_state)

# The frozen brain safely evaluates the FUTURE without chasing a moving target
# We use torch.no_grad() to save massive amounts of RAM and computation
with torch.no_grad():
    future_predictions = target_net(dummy_next_state)
    max_future_q = torch.max(future_predictions)

print(f"Active Policy Current Q-Values: {current_predictions.detach().numpy()}")
print(f"Frozen Target Max Future Value:  {max_future_q.item():.4f}")

# Simulating the network sync that happens every N steps (e.g., every 1000 frames)
print("\nInitiating Network Synchronization Protocol...")
target_net.load_state_dict(policy_net.state_dict())
print("Status: Target Network successfully updated with new Policy weights.")