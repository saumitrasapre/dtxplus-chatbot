from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from typing import Literal, Optional

from django.conf import settings


def get_llm(category: Optional[Literal["entities_tool", "summary_tool"]] = None):
    if category == "entities_tool":
        LLM_PROPERTIES = {
            "TYPE": settings.ENTITIES_TOOL_LLM_TYPE,
            "MODEL": settings.ENTITIES_TOOL_LLM_MODEL,
            "API_KEY": settings.ENTITIES_TOOL_LLM_API_KEY,
        }
    elif category == "summary_tool":
        LLM_PROPERTIES = {
            "TYPE": settings.SUMMARY_TOOL_LLM_TYPE,
            "MODEL": settings.SUMMARY_TOOL_LLM_MODEL,
            "API_KEY": settings.SUMMARY_TOOL_LLM_API_KEY,
        }
    else:
        LLM_PROPERTIES = {
            "TYPE": settings.LLM_TYPE,
            "MODEL": settings.LLM_MODEL,
            "API_KEY": settings.LLM_API_KEY,
        }

    if LLM_PROPERTIES['TYPE'] == "google_genai":
        llm = ChatGoogleGenerativeAI(
            model=LLM_PROPERTIES['MODEL'], api_key=LLM_PROPERTIES['API_KEY']
        )
    elif LLM_PROPERTIES['TYPE'] == "openai":
        llm = ChatOpenAI(model=LLM_PROPERTIES['MODEL'], api_key=LLM_PROPERTIES['API_KEY'])
    elif LLM_PROPERTIES['TYPE'] == "anthropic":
        llm = ChatAnthropic(model=LLM_PROPERTIES['MODEL'], api_key=LLM_PROPERTIES['API_KEY'])
    else:
        llm = None
    return llm


def my_function(option: Optional[Literal["option1", "option2"]] = None):
    if option == "option1":
        print("You chose option 1")
    elif option == "option2":
        print("You chose option 2")
    else:
        print("No option chosen")
