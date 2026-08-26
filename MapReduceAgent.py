# Phase 3, Day 29: Agentic Map-Reduce (Context Window Optimization)
import math

print("--- Booting Map-Reduce Context Compression Engine ---")

class MapReduceSummarizer:
    def __init__(self, max_tokens_per_chunk=50):
        self.chunk_limit = max_tokens_per_chunk
        
    def _chunk_document(self, text):
        """Splits a massive text payload into safe, manageable arrays based on a token/word limit."""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_limit):
            chunk_segment = " ".join(words[i:i + self.chunk_limit])
            chunks.append(chunk_segment)
            
        print(f"[Engine] Document fragmented into {len(chunks)} isolated context blocks.")
        return chunks

    def _mock_llm_summarize(self, text, phase="MAP"):
        """Simulates an LLM reading text and compressing its meaning."""
        # In a real environment, this makes an API call to OpenAI/Anthropic
        words = text.split()
        if len(words) == 0: return ""
        
        # Simulating compression: grabbing the first and last word to represent a 'summary'
        summary = f"{words[0]}...{words[-1]}"
        print(f"[{phase} Phase] Compressed {len(words)} words -> LLM Summary Output: '{summary}'")
        return summary

    def execute_map_reduce(self, massive_document):
        print("\n[System] Initiating Map-Reduce Sequence...")
        
        # Step 1: Fragment the document to avoid Token Overflow
        chunks = self._chunk_document(massive_document)
        
        # Step 2: The MAP Phase (Parallelizable)
        mapped_summaries = []
        for index, chunk in enumerate(chunks):
            print(f"\nProcessing Chunk {index + 1}/{len(chunks)}...")
            summary = self._mock_llm_summarize(chunk, phase="MAP")
            mapped_summaries.append(summary)
            
        # Step 3: The REDUCE Phase
        print("\n[System] Map Phase complete. Initiating Reduce aggregation...")
        combined_summaries = " ".join(mapped_summaries)
        
        final_master_summary = self._mock_llm_summarize(combined_summaries, phase="REDUCE")
        return final_master_summary

# --- Execution Environment ---
agent = MapReduceSummarizer(max_tokens_per_chunk=10)

# Simulating a large text payload that exceeds the AI's small processing window
enterprise_document = (
    "The multi-agent reinforcement learning system was deployed across the urban infrastructure to "
    "monitor localized pollution levels. Initial results demonstrated a 40% reduction in response time "
    "when micro-drones were utilized in swarm formations. The neural network efficiently rerouted paths "
    "based on real-time topological sensor data."
)

final_output = agent.execute_map_reduce(enterprise_document)

print("\n--- Final Aggregated Master Summary ---")
print(final_output)
print("\nStatus: Map-Reduce pipeline executed. Context window limits mathematically bypassed.")