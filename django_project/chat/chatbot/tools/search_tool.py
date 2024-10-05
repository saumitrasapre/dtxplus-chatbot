from ..common.common import set_env_if_not_exists
from langchain_community.tools.tavily_search import TavilySearchResults
from django.conf import settings

def get_search_tool():
    set_env_if_not_exists(key="TAVILY_API_KEY", value=settings.TAVILY_API_KEY)
    tool_description = "A search engine optimized for comprehensive, accurate, and trusted results, useful when you need to answer questions and research topics about general health, ailments and lifestyle. Strictly cannot be used to research any other topics. Input should be a search query."
    search_tool = TavilySearchResults(description=tool_description,max_results=2)
    return search_tool