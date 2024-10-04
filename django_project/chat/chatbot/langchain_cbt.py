from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from langgraph.checkpoint.memory import MemorySaver
# from langgraph.checkpoint.postgres import PostgresSaver

from .llm_backends import get_llm
from .tools.search_tool import get_search_tool
from langgraph.prebuilt import ToolNode, tools_condition

### BASIC AI AGENT ###
class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)
# Bot LLM
llm = get_llm()
# Bot search tool
search_tool = get_search_tool()
# Bot Memory
memory = MemorySaver()
# DB_URI = "postgres://<username>:<password>@localhost:5432/<dbname>?sslmode=disable"
# checkpointer = PostgresSaver.from_conn_string(DB_URI)

available_tools = [search_tool]
llm_with_tools = llm.bind_tools(available_tools)



### DEFINE NODES ###

# Chatbot node
def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Tool node
tool_node = ToolNode(tools=available_tools)


### ADD NODES TO GRAPH ###
# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("my_tools", tool_node)


### ADD EDGES TO CONNECT NODES ###
# The `route_tools` function returns "tools" if the chatbot asks to use a tool, and "END" if
# it is fine directly responding. This conditional routing defines the main agent loop.
graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
    # The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node
    # It defaults to the identity function, but if you
    # want to use a node named something else apart from "tools",
    # You can update the value of the dictionary to something else
    # e.g., "tools": "my_tools"
    {"tools": "my_tools", END: END},
)


# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("my_tools", "chatbot")
graph_builder.add_edge(START, "chatbot")


### COMPILE BUILT GRAPH ###
graph = graph_builder.compile(checkpointer=memory)
config = {"configurable": {"thread_id": "1"}}
def stream_graph_updates(user_input: str):
    for event in graph.stream({"messages": [("user", user_input)]},config):
        for value in event.values():
            value["messages"][-1].pretty_print()



# while True:
#     try:
#         user_input = input("User: ")
#         if user_input.lower() in ["quit", "exit", "q"]:
#             print("Goodbye!")
#             break

#         stream_graph_updates(user_input)
#     except:
#         # fallback if input() is not available
#         user_input = "What do you know about LangGraph?"
#         print("User: " + user_input)
#         stream_graph_updates(user_input)
#         break