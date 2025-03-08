import json
import os
from openai import OpenAI
from pydantic import BaseModel


class ResponseStructure(BaseModel):
    expressed_response: str
    companion_insights: str
    self_insights: str
                        
class LLMClient:
    client = OpenAI()

    def __init__(self, model="gpt-4o"):
        self.model = model
        self.response_format = ResponseStructure
        OpenAI.api_key = os.getenv("OPENAI_API_KEY")

    def generate_response(self, user_input):
        try:
            response = self.client.beta.chat.completions.parse(
                model=self.model,
                messages=user_input,
                response_format=self.response_format
            )
            message = response.choices[0].message
            return message.parsed
        except Exception as e:
            return f"Error: {str(e)}"

