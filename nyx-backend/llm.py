import os
import openai

class LLM:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Correct way to initialize

    def generate_response(self, user_input):
        """Generates a response using the selected model."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": user_input}],
                max_tokens=100,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ Error: {str(e)}"

