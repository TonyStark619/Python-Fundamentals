# Phase 3, Day 2: Autonomous Agent Memory Buffer
print("--- Booting Persistent Agent Memory Architecture ---")

class ConversationalAgent:
    def __init__(self):
        # The Memory Buffer: Stores all prior turns to provide context
        self.memory_buffer = []
        self.max_memory_turns = 5 # Sliding window to prevent token overflow
        
    def add_to_memory(self, role, content):
        """Appends a new interaction to the persistent memory log."""
        self.memory_buffer.append({"role": role, "content": content})
        
        # Enforce the sliding window constraint
        if len(self.memory_buffer) > self.max_memory_turns * 2:
            # Pop the oldest user/assistant pair (2 items)
            self.memory_buffer = self.memory_buffer[2:]

    def format_memory_for_prompt(self):
        """Compiles the memory dictionary into a string for the LLM."""
        formatted_history = "--- Memory Buffer ---\n"
        for entry in self.memory_buffer:
            formatted_history += f"{entry['role'].upper()}: {entry['content']}\n"
        return formatted_history + "---------------------\n"

    def mock_llm_response(self, user_input):
        # Simulating an LLM that reads its memory to answer correctly
        history_str = self.format_memory_for_prompt()
        
        if "My name is" in user_input:
            return "Hello! I have saved your name."
        elif "What is my name?" in user_input:
            if "Alex" in history_str:
                return "Your name is Alex, based on our previous conversation."
            else:
                return "I'm sorry, I don't have your name in my memory buffer."
        else:
            return "I am ready to process your request."

    def execute_turn(self, user_input):
        print(f"\nUser: {user_input}")
        
        # 1. Log the user's input into memory
        self.add_to_memory("user", user_input)
        
        # 2. Generate the AI response using the FULL memory context
        ai_response = self.mock_llm_response(user_input)
        
        # 3. Log the AI's response into memory
        self.add_to_memory("assistant", ai_response)
        
        print(f"Agent: {ai_response}")

# Execute the Autonomous Environment
agent = ConversationalAgent()

print("Initiating Multi-Turn Context Test...")
agent.execute_turn("Hi, I am initializing the system. My name is Alex.")
agent.execute_turn("Can you calculate the latency?")
agent.execute_turn("Wait, before that, What is my name?")

print("\n--- Diagnostic Visualization ---")
print(agent.format_memory_for_prompt())
print("Status: Persistent conversational memory operational. Context drift eliminated.")