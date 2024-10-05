from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.messages import trim_messages

from langgraph.checkpoint.postgres import PostgresSaver

from .llm_backends import get_llm
from .tools.search_tool import get_search_tool
from .tools.user_data_tool import get_user_info_tool
from .tools.entities_tool import get_entities_tool
from .memory.mem_initializers import get_db_uri,iniialize_postgres,get_RAM_memory
from .memory.mem_operations import clear_memory

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
user_info_tool = get_user_info_tool()
entities_tool = get_entities_tool()
available_tools = [search_tool, user_info_tool, entities_tool]
llm_with_tools = llm.bind_tools(available_tools)

# Initialize bot memory
iniialize_postgres()



### DEFINE NODES ###

# Chatbot node
def chatbot(state: State):
    # Message trimming strategy to optimize memory - 
    
    trimmed_messages = trim_messages(
    state["messages"],
    # Keep the last <= n_count tokens of the messages.
    strategy="last",
    token_counter=len,
    # When token_counter=len, each message
    # will be counted as a single token.
    # Remember to adjust for your use case
    max_tokens=20,
    # Most chat models expect that chat history starts with either:
    # (1) a HumanMessage or
    # (2) a SystemMessage followed by a HumanMessage
    start_on="human",
    # Most chat models expect that chat history ends with either:
    # (1) a HumanMessage or
    # (2) a ToolMessage
    end_on=("human", "tool"),
    # Usually, we want to keep the SystemMessage
    # if it's present in the original history.
    # The SystemMessage has special instructions for the model.
    include_system=True,
    )

    return {"messages": [llm_with_tools.invoke(trimmed_messages)]}

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

def invoke_graph_updates(user_input: str, thread_id = '1'):
    DB_URI = get_db_uri()
    with PostgresSaver.from_conn_string(DB_URI) as memory:
        graph = graph_builder.compile(checkpointer=memory)
        config = {"configurable": {"thread_id": str(thread_id)}}
        res = []
        # clear_memory(thread_id='1')
        for event in graph.stream({"messages": [("user", user_input)]},config):
            for value in event.values():
                res.append(value)
    return res




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