import requests
import json
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()



# First API call with reasoning
response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": os.getenv("MODEL_NAME"),
    "messages": [
        {
          "role": "user",
          "content": "How many r's are in the word 'strawberry'?"
        }
      ],
    "reasoning": {
        "enabled": True,
        "effort":  "minimal"
        }
  })
)
print(response.text)

# \"max\"|\"xhigh\"|\"high\"|\"medium\"|\"low\"|\"minimal\"|\"none\"",

print(response.json()["choices"][0]["message"]["content"])

# # Extract the assistant message with reasoning_details
# response = response.json()
# response = response["choices"][0]["message"]

# # Preserve the assistant message with reasoning_details
# messages = [
#   {
#     "role": "user", 
#     "content": "How many r's are in the word 'strawberry'?"
#   },
#   { 
#     "role": "assistant",
#     "content": response.get("content"),
#     # "reasoning_details": response.get('reasoning_details')  # Pass back unmodified
#   },
#   {
#     "role": "user", 
#     "content": "Are you sure? Think carefully."
#   }
# ]


# # Second API call - model continues reasoning from where it left off
# response2 = requests.post(
#   url="https://openrouter.ai/api/v1/chat/completions",
#    headers={
#       "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
#       "Content-Type": "application/json",
#     },
#   data=json.dumps({
#     "model": os.getenv("MODEL_NAME"),
#     "messages": messages,  # Includes preserved reasoning_details
#     "reasoning": {"enabled": False}
#   })
# )

# print(response2.json()["choices"][0]["message"]["content"])