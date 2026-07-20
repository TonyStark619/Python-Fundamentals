# Phase 2, Day 42: Deep Reinforcement Learning (DQN)
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

print("--- Booting Deep Q-Network (DQN) Architecture ---")

# 1. The AI Brain (Predicts future rewards based on the current state)
class DQNAgent(nn.Module):
    def __init__(self, state_features, num_actions):
        super().__init__()
        # e.g., State could be 4 sensor readings from a robot
        # Actions could be 2 choices (Move Left, Move Right)
        self.brain = nn.Sequential(
            nn.Linear(in_features=state_features, out_features=24),
            nn.ReLU(),
            nn.Linear(in_features=24, out_features=24),
            nn.ReLU(),
            nn.Linear(in_features=24, out_features=num_actions) 
        )

    def forward(self, state_tensor):
        # Outputs the predicted Q-Value for every possible action
        return self.brain(state_tensor)

# 2. Initialize the Architecture
state_size = 4
action_size = 2
agent = DQNAgent(state_size, action_size)
optimizer = optim.Adam(agent.parameters(), lr=0.001)

# Simulating an environmental interaction step
# The robot's sensors read a state (e.g., [1.0, 0.5, -0.2, 0.1])
current_state = torch.tensor([[1.0, 0.5, -0.2, 0.1]])

print("Executing Environmental State Analysis...")
# The AI predicts the rewards for Action 0 (Left) and Action 1 (Right)
predicted_q_values = agent(current_state)

print(f"\nPredicted Q-Values Matrix: {predicted_q_values.detach().numpy()}")
print(f"Action 0 (Left) Reward Prediction:  {predicted_q_values[0][0]:.4f}")
print(f"Action 1 (Right) Reward Prediction: {predicted_q_values[0][1]:.4f}")

# The AI greedily selects the action with the highest mathematical prediction
best_action = torch.argmax(predicted_q_values).item()
print(f"\nAI Decision: Executing Action {best_action}")

print("\nStatus: Neural Q-Value prediction operational. Ready for Bellman loss optimization.")