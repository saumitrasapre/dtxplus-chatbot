from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

from django.conf import settings

def get_llm():
    if settings.LLM_TYPE == "google_genai":
        llm = ChatGoogleGenerativeAI(
            model=settings.LLM_MODEL, api_key=settings.LLM_API_KEY
        )
    elif settings.LLM_TYPE == "openai":
        llm = ChatOpenAI(model=settings.LLM_MODEL, api_key=settings.LLM_API_KEY)
    elif settings.LLM_TYPE == "anthropic":
        llm = ChatAnthropic(model=settings.LLM_MODEL, api_key=settings.LLM_API_KEY)
    else:
        llm = None

    return llm



