from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

class DSAState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatGroq(model="llama-3.1-8b-instant")

DSA_MENTOR_PROMPT = """
You are an expert DSA mentor.

When a user gives a problem:
1. Identify pattern (two pointers, DP, graph, etc.)
2. Explain intuition in simple words
3. Give brute force approach
4. Give optimized approach
5. Provide clean code (Python)
6. Give time & space complexity
7. Suggest 2 similar problems
Keep explanation beginner friendly.
"""

def dsa_node(state: DSAState):
    messages = state["messages"]
    system_msg = SystemMessage(content=DSA_MENTOR_PROMPT)
    response = llm.invoke([system_msg] + messages)
    return {"messages": [response]}

memory = MemorySaver()

graph = StateGraph(DSAState)
graph.add_node("dsa_mentor", dsa_node)
graph.add_edge(START, "dsa_mentor")
graph.add_edge("dsa_mentor", END)

chatbot = graph.compile(checkpointer=memory)

def stream_ai_response(user_text: str, thread_id: str):
    events = chatbot.stream(
        {"messages": [HumanMessage(content=user_text)]},
        config={"configurable": {"thread_id": thread_id}},
        stream_mode="messages",
    )
    for event in events:
        if event[0].content:
            yield event[0].content
