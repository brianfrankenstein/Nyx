import json
from llm_client import LLMClient
from structured_output import parse_structured_response

class Brain:
    def __init__(self):
        self.history = []         # Session conversation history
        self.memory_store = []    # For additional memory elements
        self.llm_client = LLMClient(model="gpt-4")  # Easily swap model here

    def handle_message(self, user_text):
        # 1. Add the user's message to history
        self.history.append({"role": "user", "content": user_text})

        # 2. (Optional) Build a prompt that includes history.
        # For now, we just use the latest user text.
        raw_output = self.llm_client.generate_response(user_text)
        
        # 3. Parse the raw LLM output into structured data
        try:
            structured_output = parse_structured_response(raw_output)
        except Exception as e:
            # Fallback: use raw text if structured output isn't available
            structured_output = {"response": raw_output, "metadata": {}}

        # 4. Process the structured output
        user_response = structured_output.get("response", raw_output)
        memory_data = structured_output.get("metadata", {}).get("memory", None)
        if memory_data:
            self.store_in_memory(memory_data)
        
        # 5. Add the assistant's response to history
        self.history.append({"role": "assistant", "content": user_response})
        
        # Return the structured output to main (entry point)
        return structured_output

    def store_in_memory(self, memory_data):
        # Here you can implement how to store and later retrieve memory parts.
        self.memory_store.append(memory_data)
