# from django.conf import settings
from ..common.common_functions import set_env_if_not_exists
from langchain_community.tools.tavily_search import TavilySearchResults


class Settings:
    LLM_TYPE = "google_genai"
    LLM_MODEL = "gemini-1.5-flash"
    LLM_API_KEY = "AIzaSyDeapQtAmO-tdgcay5_gl2K4w3rc0s6W6k"
    TAVILY_API_KEY = "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"


settings = Settings()


def get_search_tool():
    set_env_if_not_exists(key="TAVILY_API_KEY", value=settings.TAVILY_API_KEY)
    tool_description = "A search engine optimized for comprehensive, accurate, and trusted results, useful when you need to answer questions and research topics about general health, ailments and lifestyle. Strictly cannot be used to research any other topics. Input should be a search query."
    search_tool = TavilySearchResults(description=tool_description,max_results=2)
    return search_tool