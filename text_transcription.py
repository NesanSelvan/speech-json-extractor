import requests
import time
def transcribe_text(text):
    url = "http://192.168.1.100:1234/v1/chat/completions/"
    startTime = time.time()
    response = requests.post(url, json={
        "model": "google/gemma-3-4b",
        "messages": [
          {
  "role": "system",
  "content": """You are a JSON extractor for grocery items. Extract items and quantities from text.

RULES:
1. Return ONLY raw JSON - no markdown, no code blocks
2. Format: {"items": [{"name": "item", "quantity": N}]}
3. If quantity not specified, assume 1
4. Word numbers count: "two" = 2, "three" = 3, "rend" = 2
5. Extract ALL nouns as items (latkan, hanging, tomato, etc.)
6. Never return code or explanations"""
},
            {
                "role": "user",
                "content": f"Extract items from: {text}"
            }
        ],
        "temperature": 0,
        "max_tokens": 150,
        "stream": False
    })
    endTime = time.time()
    print(f"Time taken: {endTime - startTime}")
    print(response.json()['choices'][0]['message']['content'])
    return response.json()['choices'][0]['message']['content']
    

