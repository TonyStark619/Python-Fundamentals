# Phase 2, Day 43: Experience Replay Buffer (DQN Stability)
import random
from collections import deque

print("--- Booting RL Memory Architecture ---")

class ReplayBuffer:
    def __init__(self, capacity):
        # A deque (Double-Ended Queue) automatically drops the oldest memories 
        # when it hits the maximum capacity.
        self.memory = deque(maxlen=capacity)

    def store_experience(self, state, action, reward, next_state, done):
        # Save the exact interaction into the ledger
        experience = (state, action, reward, next_state, done)
        self.memory.append(experience)

    def sample_batch(self, batch_size):
        # Mathematically sample a random subset of past experiences 
        # to prevent the neural network from overfitting to recent events.
        return random.sample(self.memory, batch_size)

    def current_size(self):
        return len(self.memory)

# Initialize the architecture (Memory Capacity: 10,000 events)
ai_memory = ReplayBuffer(capacity=10000)

print("Simulating Environmental Interactions...")

# Simulating 5 rapid interactions (e.g., frames of a video game)
for frame in range(5):
    # Dummy data: State, Action, Reward, Next State, Game Over?
    ai_memory.store_experience(
        state=f"ScreenPixels_Frame_{frame}", 
        action=random.choice(["Left", "Right", "Jump"]), 
        reward=10, 
        next_state=f"ScreenPixels_Frame_{frame+1}", 
        done=False
    )

print(f"Memory Buffer Size: {ai_memory.current_size()} stored events.")

print("\nInitiating Training Optimization Step...")
# The Neural Network decides it's time to learn, so it pulls a random batch of 3 past events
batch_size = 3
training_batch = ai_memory.sample_batch(batch_size)

print(f"Randomized Training Batch Extracted (Size {batch_size}):")
for i, experience in enumerate(training_batch):
    print(f"  Event {i+1}: Action '{experience[1]}' resulted in Reward {experience[2]}")

print("\nStatus: Experience Replay Buffer active. Catastrophic forgetting neutralized.")