# 🧠 Intelligent Search Agent (ReAct + Tools + Memory)

A conversational AI agent that can **reason, search the web, and retrieve academic papers** using a ReAct-based tool-using architecture powered by LangGraph.

---

## 🚀 Live Demo
https://intelligent-search-agent.streamlit.app/

---

## 📌 Key Features

- 🧠 ReAct agent (Reasoning + Tool execution loop)
- 🌐 Real-time web search using DuckDuckGo
- 📚 Academic paper search using Arxiv API
- 💬 Multi-turn conversational memory (LangGraph MemorySaver)
- ⚡ Streamlit chat-based UI
- 🔄 Session reset functionality

---

## 🏗️ Architecture

User Query  
→ Streamlit UI  
→ LangGraph ReAct Agent  
→ LLM (Qwen via Groq API)  
→ Tool Selection:
   - Web Search (DuckDuckGo)
   - Arxiv Research Search  
→ MemorySaver (conversation state)  
→ Final Response

---

## 🛠️ Tech Stack

- Python  
- Streamlit  
- LangChain  
- LangGraph  
- Groq API (Qwen model)  
- DuckDuckGo Search (DDGS)  
- Arxiv API  

---

## 🧠 Tools Used

### 🔍 Web Search Tool
- Uses DuckDuckGo (DDGS)
- Returns latest web snippets

### 📚 Arxiv Tool
- Fetches research papers
- Returns title + abstract summary

---

## 💬 How It Works

1. User enters a query  
2. LLM decides whether a tool is needed  
3. Agent calls:
   - Web Search OR
   - Arxiv Search OR
   - Direct reasoning  
4. Response is generated  
5. Conversation is stored using memory  

---

## 🔁 Memory Feature

- Uses `LangGraph MemorySaver`
- Maintains conversation context per session
- Supports multi-turn dialogue

---

## 📦 Installation

```bash
git clone https://github.com/sudarshanjha-dev/Intelligent-Search-Agent.git
cd Intelligent-Search-Agent
pip install -r requirements.txt
streamlit run app.py
