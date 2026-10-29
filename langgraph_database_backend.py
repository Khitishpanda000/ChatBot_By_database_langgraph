from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_ollama import ChatOllama 
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

llm = ChatOllama(model="llama3.2:latest", temperature=0)

class ChartState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

def chart_node(state: ChartState):
    message = state["messages"]
    response = llm.invoke(message)

    return {'messages': response}

connection = sqlite3.connect(database='chatbot.db', check_same_thread=False)

#checkpointer
checkPointer = SqliteSaver(conn=connection) 

graph = StateGraph(ChartState)

graph.add_node("chart_node", chart_node)

graph.add_edge(START, "chart_node")
graph.add_edge("chart_node", END)

chatbot = graph.compile(checkpointer=checkPointer)


def retriver_all_threads():
    all_thread = set()

    for checkpoint in checkPointer.list(None):
        all_thread.add(checkpoint.config["configurable"]["thread_id"])

    return (list(all_thread))