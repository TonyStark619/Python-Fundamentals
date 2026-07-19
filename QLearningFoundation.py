# Phase 2, Day 41: Reinforcement Learning (Q-Table Updates)
import numpy as np

print("--- Booting Reinforcement Learning Q-Engine ---")

# 1. Initialize the Q-Table (The AI's Brain Ledger)
# Imagine a tiny grid world: 3 States (Locations) and 2 Actions (Left or Right)
# The AI starts knowing absolutely nothing, so the ledger is all zeros.
num_states = 3
num_actions = 2
q_table = np.zeros((num_states, num_actions))

# 2. Define the Hyperparameters
learning_rate = 0.1   # How quickly the AI abandons old beliefs for new information
discount_factor = 0.9 # How much the AI cares about long-term future rewards vs immediate gratification

# Simulating an interaction with the environment:
# The AI was in State 0, chose Action 1 (Right), and landed in State 1.
current_state = 0
action_taken = 1
reward_received = 10  # The environment rewarded the AI
next_state = 1

print("Executing Environmental Interaction...")
print(f"Agent moved from State {current_state} -> State {next_state} via Action {action_taken}. Reward: {reward_received}")

# 3. The Bellman Equation (Updating the AI's Brain)
# The AI looks at the new state, finds the maximum possible future reward it could get from there,
# and works backward to update the value of the action it just took.

# What is the highest Q-value available in the new state?
max_future_q = np.max(q_table[next_state])

# What is the current Q-value of the action we just took?
current_q = q_table[current_state, action_taken]

# Calculate the new, updated Q-value
new_q = (1 - learning_rate) * current_q + learning_rate * (reward_received + discount_factor * max_future_q)

# Write the new intelligence into the ledger
q_table[current_state, action_taken] = new_q

print("\n--- AI Memory Ledger (Q-Table) Updated ---")
print(q_table)
print("\nStatus: Bellman update successful. The AI now mathematically prefers Action 1 in State 0.")