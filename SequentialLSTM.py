# Phase 2, Day 26: Sequence Memory & LSTM Architecture
import torch
import torch.nn as nn

print("--- Booting Recurrent NLP Architecture ---")

class SequenceProcessor(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        # 1. Translate integer IDs into dense vectors
        self.embedding = nn.Embedding(num_embeddings=vocab_size, embedding_dim=embed_dim)
        
        # 2. The Memory Engine (LSTM)
        # batch_first=True tells PyTorch our data format is [Batch, Sequence_Length, Features]
        self.lstm = nn.LSTM(input_size=embed_dim, hidden_size=hidden_dim, batch_first=True)
        
        # 3. The Decision Maker (e.g., Sentiment Analysis: Positive vs Negative)
        self.fc = nn.Linear(in_features=hidden_dim, out_features=2)

    def forward(self, sentence_tensor):
        # Step A: Convert words to mathematical vectors
        embedded = self.embedding(sentence_tensor)
        print(f"1. Embedded Matrix Shape: {list(embedded.shape)}")
        
        # Step B: Pass the sequence through the LSTM conveyor belt
        # It outputs all step predictions (lstm_out) and the final memory state (hidden_state)
        lstm_out, (hidden_state, cell_state) = self.lstm(embedded)
        
        # We only care about the very last memory state after it has read the entire sentence
        final_memory = hidden_state[-1]
        print(f"2. Final Memory State Extracted: {list(final_memory.shape)}")
        
        # Step C: Make a final classification based on that memory
        return self.fc(final_memory)

# Initialize the architecture (Vocab: 1000 words, Vectors: 16D, Memory: 32D)
ai_model = SequenceProcessor(vocab_size=1000, embed_dim=16, hidden_dim=32)

# Simulating 1 batch of data containing 1 sentence with 5 words (e.g., "The future is artificial intelligence")
mock_sentence = torch.tensor([[45, 892, 12, 401, 755]])

print("\nExecuting Sequential Inference Protocol...")
output_prediction = ai_model(mock_sentence)

print("\n--- Model Output ---")
print(f"Final Output Logits: {output_prediction.detach().numpy()}")
print("Status: Temporal sequence successfully processed with memory retention.")