import os, json, sys, re, datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Ensure UTF-8 output on Windows consoles
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

load_dotenv()

# Dual provider configuration (Gemini + OpenRouter)
PROVIDERS = {}

gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
if gemini_key:
    PROVIDERS["gemini"] = {
        "client": OpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=gemini_key,
            timeout=60.0,
        ),
        "model": os.environ.get("GEMINI_MODEL", "gemini-3.7-flash"),
    }

openrouter_key = os.environ.get("OPENROUTER_API_KEY", "").strip()
if openrouter_key:
    PROVIDERS["openrouter"] = {
        "client": OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=openrouter_key,
            timeout=60.0,
        ),
        "model": os.environ.get("OPENROUTER_MODEL") or os.environ.get("MODEL") or "nvidia/nemotron-3.5-lightning:free",
    }

PREFERRED_PROVIDER = os.environ.get("PROVIDER", "gemini" if "gemini" in PROVIDERS else "openrouter").lower()

def sanitize_messages(messages):
    """
    Normalizes messages across providers so that:
    - content is never None (which causes Gemini 400 'Value is not a string: null')
    - provider-specific null fields are omitted
    """
    cleaned = []
    for m in messages:
        if hasattr(m, "model_dump"):
            d = m.model_dump()
        elif isinstance(m, dict):
            d = dict(m)
        else:
            d = dict(m)
        if d.get("content") is None:
            d["content"] = ""
        # Keep only standard fields with non-null values
        allowed = {"role", "content", "tool_calls", "tool_call_id", "name"}
        d = {k: v for k, v in d.items() if k in allowed and v is not None}
        cleaned.append(d)
    return cleaned

def call_chat_completion(messages, tools, active_provider):
    """
    Calls chat completions with the active provider.
    If a rate limit (429), quota issue, or high load (503) occurs,
    it automatically falls back to the other configured provider.
    """
    fallback = "openrouter" if active_provider == "gemini" else "gemini"
    providers_to_try = [p for p in [active_provider, fallback] if p in PROVIDERS]

    if not providers_to_try:
        raise RuntimeError("No LLM provider configured. Set GEMINI_API_KEY or OPENROUTER_API_KEY in .env.")

    prepared_msgs = sanitize_messages(messages)

    last_err = None
    for prov_name in providers_to_try:
        prov = PROVIDERS[prov_name]
        try:
            resp = prov["client"].chat.completions.create(
                model=prov["model"],
                messages=prepared_msgs,
                tools=tools,
                temperature=0,
            )
            return resp, prov_name
        except Exception as e:
            err_str = str(e).lower()
            if any(k in err_str for k in ["rate limit", "429", "503", "quota", "resource_exhausted"]):
                print(f"\n[Provider Alert] Rate limit or high load on '{prov_name}'. Attempting fallback to '{fallback}'...")
                last_err = e
                continue
            raise e
    raise last_err

SANDBOX = (Path(__file__).parent / "docs").resolve()
MAX_STEPS = 8

# ---------- tools ----------
def search_docs(query):
    # Extract query words, filtering out common filler words
    words = re.findall(r"\w+", query.lower())
    stopwords = {"when", "what", "where", "which", "who", "how", "is", "are", "was", "were", "the", "a", "an", "in", "on", "at", "for", "to", "of", "and", "or", "it", "did", "do", "does"}
    keywords = [w for w in words if w not in stopwords] or words

    scores = {}
    for f in SANDBOX.glob("*.md"):
        try:
            text = f.read_text(encoding="utf-8").lower()
            match_count = sum(1 for w in keywords if w in text)
            if match_count > 0:
                scores[f.name] = match_count
        except Exception:
            pass

    if not scores:
        return "No matching documents."

    # Return top matches ranked by relevance
    sorted_hits = sorted(scores.keys(), key=lambda k: scores[k], reverse=True)
    best_score = scores[sorted_hits[0]]
    hits = [k for k in sorted_hits if scores[k] >= max(1, best_score - 1)][:5]
    return hits or sorted_hits[:5]

def read_doc(filename):
    clean_name = Path(filename).name
    path = (SANDBOX / clean_name).resolve()
    if not path.is_file() or SANDBOX not in path.parents:
        raise ValueError(f"Document '{filename}' not found or access denied")
    return path.read_text(encoding="utf-8")

TOOLS_FN = {"search_docs": search_docs, "read_doc": read_doc}
TOOLS = [
  {"type": "function", "function": {
     "name": "search_docs",
     "description": "Keyword search over company docs. Returns matching filenames.",
     "parameters": {"type": "object",
                    "properties": {"query": {"type": "string"}},
                    "required": ["query"]}}},
  {"type": "function", "function": {
     "name": "read_doc",
     "description": "Read the full text of one document by filename.",
     "parameters": {"type": "object",
                    "properties": {"filename": {"type": "string"}},
                    "required": ["filename"]}}},
]

# ---------- the loop ----------
def run_agent(question):
    today_str = datetime.date.today().strftime("%B %d, %Y")
    messages = [
      {"role": "system", "content": f"You are an assistant for Acme Robotics. Today's date is {today_str}. Answer using only the company docs. You MUST use search_docs and read_doc to retrieve facts before answering. If the docs don't contain the answer, say so clearly."},
      {"role": "user", "content": question},
    ]
    current_provider = PREFERRED_PROVIDER
    active_model = PROVIDERS.get(current_provider, {}).get("model", "unknown")
    print(f"\n[Using provider: {current_provider.upper()} | Model: {active_model}]")
    for step in range(1, MAX_STEPS + 1):
        resp, used_provider = call_chat_completion(messages, TOOLS, current_provider)
        if used_provider != current_provider:
            print(f"[Switched active provider to: {used_provider}]")
            current_provider = used_provider

        msg = resp.choices[0].message
        messages.append(msg)                       # keep the model's turn in history
        print(f"\n[step {step}] model ({used_provider}) said: {msg.content!r}")

        if not msg.tool_calls:                     # no tool asked -> final answer
            return msg.content

        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments)
            print(f"[step {step}] tool call: {name}({args})")
            try:
                result = TOOLS_FN[name](**args)
            except Exception as e:                 # stretch goal handled here
                result = f"ERROR: {e}"
            print(f"[step {step}] tool result: {str(result)[:200]}")
            messages.append({"role": "tool", "tool_call_id": call.id,
                             "content": json.dumps(result) if not isinstance(result, str) else result})
    return "Stopped: hit MAX_STEPS without a final answer."

if __name__ == "__main__":
    print("\nFINAL:", run_agent(input("Question: ")))