import os, json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
provider = os.environ.get("PROVIDER", "gemini").lower()
if provider == "gemini" and os.environ.get("GEMINI_API_KEY"):
    client = OpenAI(
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        api_key=os.environ["GEMINI_API_KEY"].strip(),
    )
    model = os.environ.get("GEMINI_MODEL", "gemini-flash-lite-latest")
else:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY", "").strip(),
    )
    model = os.environ.get("OPENROUTER_MODEL") or os.environ.get("MODEL", "poolside/laguna-s-2.1:free")

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    },
}]

resp = client.chat.completions.create(
    model=model,
    messages=[{"role": "user", "content": "What's the weather in Pune?"}],
    tools=tools,
)
msg = resp.choices[0].message
print(msg.tool_calls)   # look at this!