# Research Agent 🔍

An AI-powered research agent that searches the web, reads pages, and gives you structured answers — all running **100% free and locally** on your laptop using Ollama.

No paid APIs. No cloud. Just your laptop doing the thinking.

---

## What it does

You ask a question. The agent:
1. **Thinks** about how to find the answer
2. **Searches** the web using Tavily
3. **Reads** the most relevant pages
4. **Thinks again** — do I have enough information?
5. **Gives you** a clean, structured final answer

All of this happens automatically in a loop called the **ReAct pattern** (Reasoning + Acting) — the same architecture used inside products like Perplexity AI and ChatGPT's browsing mode.

---

## Demo

```
What do you want me to research?
> What are the latest AI agent frameworks in 2024?

--- Step 1 ---
[LLM]: Thought: I need to search for recent AI agent frameworks.
       Action: search_web
       Input: best AI agent frameworks 2024

[TOOL CALL]: search_web('best AI agent frameworks 2024')
[OBSERVATION]: Found 3 results...

--- Step 2 ---
[LLM]: Thought: Let me read the most detailed article.
       Action: scrape_page
       Input: https://example.com/ai-frameworks

--- Step 3 ---
[LLM]: Thought: I have enough information now.
       Action: FINISH
       Input: Here are the top AI agent frameworks in 2024...

[FINAL ANSWER]:
The top AI agent frameworks in 2024 are...
```

---

## Architecture

```
You (ask a question)
        │
        ▼
   main.py  ──────────────────────────────────────┐
        │                                          │
        ▼                                          │
   agent.py  (ReAct Loop)                          │
   ┌─────────────────────────┐                     │
   │  1. Thought  (LLM)      │◄── Ollama running  │
   │  2. Action   (tool)     │    locally on      │
   │  3. Observation (result)│    your laptop     │
   │  4. Loop until done     │                    │
   └─────────────────────────┘                     │
        │                                          │
        ▼                                          │
   tools.py                                        │
   ├── search_web()  ──► Tavily API (web search)  │
   └── scrape_page() ──► BeautifulSoup (reading)  │
        │                                          │
        ▼                                          │
   Final Answer printed to terminal ───────────────┘
```

---

## Tech Stack

| Tool | What it does | Cost |
|---|---|---|
| [Ollama](https://ollama.com) | Runs LLaMA 3.2 locally on your laptop | Free forever |
| [Tavily](https://tavily.com) | Searches the web for real-time info | Free (1000/month) |
| [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) | Reads and cleans webpage content | Free |
| Python | Glues everything together | Free |

---

## Project Structure

```
Research_Agent/
│
├── main.py           ← entry point — run this
├── agent.py          ← ReAct loop brain
├── tools.py          ← search and scrape functions
├── prompts.py        ← system prompt for the LLM
├── requirements.txt  ← all libraries needed
└── .env              ← your API keys (never uploaded)
```

---

## Setup & Run

### 1. Clone the repo

```bash
git clone https://github.com/23f2002523/Research_Agent.git
cd Research_Agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install Ollama and download the model

Download Ollama from [ollama.com](https://ollama.com) then run:

```bash
ollama pull llama3.2
```

This downloads the AI model (~2GB) to your laptop. One time only.

### 4. Get your free Tavily API key

Sign up at [tavily.com](https://tavily.com) — free, no credit card needed.

### 5. Create your .env file

Create a file called `.env` in the project folder:

```
TAVILY_API_KEY=your_tavily_key_here
```

### 6. Run the agent

```bash
python main.py
```

Then type any research question and watch it work.

---

## How it works — the ReAct pattern

Most AI tools just answer from memory. This agent **actually goes and checks** before answering.

The ReAct loop forces the LLM to follow this pattern every single step:

```
Thought    →   "I need to search for X"
Action     →   search_web("X")
Observation →  "Here are the results..."
Thought    →   "I should read this article for more detail"
Action     →   scrape_page("https://...")
Observation →  "The article says..."
Thought    →   "I have enough info now"
Action     →   FINISH → gives final answer
```

This makes the agent reliable — it cannot hallucinate an answer because it is forced to gather real information before concluding.

---

## What I learned building this

- How the **ReAct pattern** works and why it prevents hallucination
- How to connect a **locally running LLM** (Ollama) to Python code
- How to write **tool functions** and give an agent new abilities
- How **web scraping** works with BeautifulSoup
- How **prompt engineering** shapes agent behaviour
- How to structure a real Python project across multiple files

---

## Roadmap

- [ ] Streamlit UI — chat interface instead of terminal
- [ ] Conversation memory — ask follow-up questions
- [ ] Save reports as PDF
- [ ] Add Wikipedia tool
- [ ] Add YouTube transcript tool
- [ ] Multi-agent version — researcher + writer + reviewer

---

## Author

**23f2002523**  
3rd Year Student — AI / ML / Data Analytics  
GitHub: [@23f2002523](https://github.com/23f2002523)

---

## License

MIT License — feel free to use, modify, and build on this.