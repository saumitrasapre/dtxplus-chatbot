from langchain_core.tools import tool
from ...models import Chat
from ..common.common import ChatInfo
from ..llm_backends import get_llm
from ..memory.mem_operations import get_latest_checkpoint_from_memory, parse_checkpoint_messages_for_UI
import json
from langchain.schema import SystemMessage, HumanMessage


@tool("summary_tool")
def summary_tool():
    """This tool is used to obtain a concise (3 line) summary of the conversation that the user has had with the bot up until now. Can be used to get a quick
    summary of the conversation. Is NOT a replacement for actual database information. Should NOT be treated as ground truth for facts."""

    summary_tool_llm = get_llm("summary_tool")

    if ChatInfo.chat_thread_id:
        c_thread_id = str(ChatInfo.chat_thread_id)
        parsed_json = parse_checkpoint_messages_for_UI(get_latest_checkpoint_from_memory(thread_id=c_thread_id)['messages'])
        system_message = SystemMessage(
            content="""You are a conversation summarizer. You will receive input in the form of a dictionary of the
            chat messages that have occurred between a user and a chatbot. Your task is to create a simple, concise summary
            not more than 3 lines of the input. The summary should be from the perspective of the bot. Rather than using "the user",
            use "you". Return the output in the form of a string.
            """
        )

        query = f"conversation up until now = {json.dumps(parsed_json)}"

        human_message = HumanMessage(content=query)

        # Send the system message and human message to the model
        output = summary_tool_llm([system_message, human_message])
        return output.content

    else:
        # User is not logged in, send blank data instead (This should not happen in the normal case)
        output = {}
        return json.dumps(output)


def summary_tool_parameterized(parsed_json):

    summary_tool_llm = get_llm("summary_tool")
    system_message = SystemMessage(
        content="""You are a conversation summarizer. You will receive input in the form of a dictionary of the
            chat messages that have occurred between a user and a chatbot. Your task is to create a simple, concise summary
            not more than 3 lines of the input. The summary should be from the perspective of the bot. Rather than using "the user",
            use "you". Return the output in the form of a string.
        """
    )

    query = f"conversation up until now = {json.dumps(parsed_json)}"

    human_message = HumanMessage(content=query)

    # Send the system message and human message to the model
    output = summary_tool_llm([system_message, human_message])
    return output.content



def get_summary_tool():
    return summary_tool
