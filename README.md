# Agents Daily 🤖

Daily AI Agent experiments, patterns, and implementations.

## Repository Structure

```
agents-daily/
├── agent-day1/          # Day 1: Document search & Q&A agent with function calling
│   ├── docs/            # Knowledge base documents
│   ├── agent.py         # Main agent loop with automatic provider fallback
│   ├── raw_call.py      # Minimal OpenAI-compatible function calling example
│   ├── .env.example     # Template environment file
│   └── requirements.txt # Python dependencies
├── .gitignore
└── README.md
```

## Day 1: Acme Robotics Docs Agent
An autonomous agent that reasons over company documentation using function calling:
- **Tools**: `search_docs` (keyword search ranking) and `read_doc` (document reader).
- **Dual Providers**: Seamless automatic fallback between **Google Gemini** (`gemini-flash-lite-latest`) and **OpenRouter** (`poolside/laguna-s-2.1:free`). If one hits a rate limit (HTTP 429), it automatically fails over to the other.

### Quick Start (Day 1)
```bash
cd agent-day1
python -m venv .venv
# Activate virtual environment:
# On Windows: .venv\Scripts\activate
# On Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
# Add your GEMINI_API_KEY or OPENROUTER_API_KEY in .env

python agent.py
```
