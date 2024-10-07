from langchain_core.tools import tool
from django.contrib.auth.models import User
from ..common.common import UserInfo
from ..llm_backends import get_llm
import json
from langchain.schema import SystemMessage, HumanMessage


@tool("entities_tool")
def entities_tool(query: str):
    """Tool used to save relevant medical entities from the user input. Takes in the user input as the query and extracts and saves and key entities related to the user's preference for appointment time, or any user mention of
    a medication or medication regimen or any diet from the conversation which the user mentioned. Should STRICTLY be called when any of these is mentioned by the user in any way, shape or form."""

    entities_tool_llm = get_llm("entities_tool")

    if UserInfo.user:
        c_usr_id = UserInfo.user.id
        current_user = User.objects.filter(id=c_usr_id).first()
        curr_add_entities = current_user.profile.additional_entities
        system_message = SystemMessage(
            content="""You are an entity extractor. You take in the user input as the query and extract
            key entities from the text which the user mentions.
            You also take in the existing list of user entities as input, and modify the attributes that exist there
            if new entities are not found.
            If new entities are found, then append them to the user entities
            Pay strict attention to the user's preference for appointment time, or any user mention of
            a medication /diet/allergy etc.
            For example if the patient says, "i am taking lisinopril twice a day" 
            then extract {"medication": "lisinopril", "frequency": "2 times a day"}. 
            Your output should be a dictionary of a list of dicts with only one key called "entities".
            Output should strictly be in json format. This is compulsory and a non-negotiable.
            There should be no other stray characters other than the json. Use minimal number of escape characters. 
            If there aren't any new entities then output the existing user entities as it is.
            """
        )

        query = f"existing_user_entities = {curr_add_entities}, user_input = " + query

        human_message = HumanMessage(content=query)

        # Send the system message and human message to the model
        output = entities_tool_llm([system_message, human_message])
        current_user.profile.additional_entities = output.content
        current_user.save()
        return json.dumps(output.content)

    else:
        # User is not logged in, send blank data instead (This should not happen in the normal case)
        curr_add_entities = {}
        system_message = SystemMessage(
            content="""You are an entity extractor. You take in the user input as the query and extract
            key entities from the text which the user mentions.
            You also take in the existing list of user entities as input, and modify the attributes that exist there
            if no new attributes are found.
            If new entities are found, then append them to the user entities
            Some examples of attributes include -  the patient's preference for appointment time, or any patient mention of
            a medication /diet / etc.
            For example if the patient says, "i am taking lisinopril
            twice a day" then extract {"medication": "lisinopril", "frequency": "2 times a day"}. 
            Your output should be a dictionary of a list of dicts with only one key called "entities".
            Output should strictly be in json format. This is compulsory and a non-negotiable.
            There should be no other stray characters other than the json. 
            If there aren't any new entities then output the existing user entities as it is.
            """
        )

        query = f"existing_user_entities = {curr_add_entities}, user_input = " + query

        human_message = HumanMessage(content=query)

        # Send the system message and human message to the model
        output = entities_tool_llm([system_message, human_message])
        return json.dumps(output.content)


def get_entities_tool():
    return entities_tool
