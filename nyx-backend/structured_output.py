import json

def parse_structured_response(raw_output):
    """
    Parses the raw LLM output into a structured dictionary.
    Expects JSON formatted output:
    
    {
      "response": "User facing message",
      "metadata": {
         "memory": { ... }   // additional data to store in memory
      }
    }
    """
    return json.loads(raw_output)
