import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_web(query: str) -> str:
    """Search the web and return top results as text."""
    results = tavily.search(query=query, max_results=3)
    
    output = ""
    for r in results["results"]:
        output += f"Title: {r['title']}\n"
        output += f"URL: {r['url']}\n"
        output += f"Summary: {r['content']}\n\n"
    
    return output


def scrape_page(url: str) -> str:
    """Fetch a webpage and return its readable text."""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        
        # remove junk tags
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        
        text = soup.get_text(separator="\n", strip=True)
        
        # return first 3000 chars to not overflow LLM context
        return text[:3000]
    
    except Exception as e:
        return f"Error scraping page: {str(e)}"


# This dict tells the agent WHAT tools exist and HOW to call them
TOOLS = {
    "search_web": {
        "function": search_web,
        "description": "Search the internet for a query. Input: a search string."
    },
    "scrape_page": {
        "function": scrape_page,
        "description": "Read full content of a URL. Input: a valid URL string."
    }
}