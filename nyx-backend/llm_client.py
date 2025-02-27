import os
import openai

class LLMClient:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_response(self, user_input):
        try:
            response = openai.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": user_input}],
                max_tokens=200,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"


