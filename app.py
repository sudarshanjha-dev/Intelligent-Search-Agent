import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.tools import tool
import arxiv
from langgraph.prebuilt import create_react_agent
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage,AIMessage
from langgraph.checkpoint.memory import MemorySaver
import uuid
import os
from dotenv import load_dotenv


load_dotenv()


#Arxiv Tool and Duckduckgo

client=arxiv.Client()
@tool
def arxivsearch(query: str) -> str:
    """Search Arxiv for research papers"""
    search = arxiv.Search(query=query, max_results=2)
    results = []
    for paper in client.results(search):
        results.append(
            f"Title: {paper.title}\n"
            f"Summary: {paper.summary[:300]}"
        )
    return "\n---\n".join(results) if results else "No papers found."


# websearch=DuckDuckGoSearchRun(name="web-search")

from ddgs import DDGS

@tool
def websearch(query: str) -> str:
    """Search the web for current information including weather news and facts."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        return "\n".join(
            [f"Title: {r['title']}\nSnippet: {r['body']}" for r in results]
        ) if results else "No results found."
    except Exception as e:
        return f"Search failed: {e}"


if "memory" not in st.session_state:
    st.session_state.memory=MemorySaver()

if "thread_id" not in st.session_state:
    st.session_state.thread_id=str(uuid.uuid4())

#Streamlit UI
st.set_page_config(
    page_title="Intelligent Search Agent",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
# 🧠 Intelligent Search Agent
### AI-powered search assistant using LLM + Web Retrieval + Reasoning

---
""")

with st.expander("🧠 How this works"):
    st.markdown("""
    1. User enters query  
    2. LLM understands intent  
    3. Web search tool retrieves data  
    4. Context is built  
    5. Final response generated using LLM  
    """)

#Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your GROQ API Key:",type="password")

if "messages" not in st.session_state:
    st.session_state['messages']=[
        {
            "role":"assistant","content":"Hi,I'm a chatbot who can search the web. How can I help you?"
        }
    ]

#Displaying chat history
for msg in st.session_state.messages:
    st.chat_message(msg['role']).write(msg['content'])



if prompt:=st.chat_input(placeholder="What is Machine Learning?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)
    if not api_key:
        st.warning("⚠️ Please enter your GROQ API Key in the sidebar")
        st.stop()

    llm=ChatGroq(groq_api_key=api_key,model_name="llama-3.1-8b-instant",streaming=False)

    tools=[arxivsearch,websearch]
    search_agent=create_react_agent(llm,tools,checkpointer=st.session_state.memory)


    with st.chat_message("assistant"):
        try:
            response=search_agent.invoke(
            {"messages":[HumanMessage(content=prompt)]},
            config={"configurable":{"thread_id":st.session_state.thread_id}}
            )
            answer = response["messages"][-1].content
        except Exception as e:
            st.error({e})
            answer="Sorry, please rephrase your question and try again"
        st.session_state.messages.append({"role":"assistant","content":answer})
        st.write(answer)
        
if st.sidebar.button("🔄 Reset Conversation"):
    st.session_state.memory = MemorySaver()
    st.session_state.thread_id = str(uuid.uuid4())
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I'm a chatbot who can search the web. How can I help you?"}
    ]
    st.rerun()
