import os
from dotenv import load_dotenv
import langgraph.graph as lg
from langgraph.prebuilt import StatefulGraph
from agents import agents
from cache import get_cached_response, cache_response

# Load API keys
load_dotenv()
GROQ_API_KEY = os.getenv("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")

# Web Search Agent with Caching
def search_web(inputs):
    query = inputs["query"]

    # Check if result is cached
    cached_result = get_cached_response(query)
    if cached_result:
        return {"search_result": cached_result}

    # If not cached, fetch data and cache it
    result = agents["web_search"].invoke(query)
    cache_response(query, result)
    return {"search_result": result}

# Finance Agent (Always Fetch Fresh Data)
def analyze_finance(inputs):
    stock_symbol = inputs.get("stock_symbol", "AAPL")  # Default: Apple

    # Always fetch fresh stock market data
    result = agents["finance"].invoke(stock_symbol)
    return {"finance_result": result}

# Create LangGraph workflow
graph = lg.Graph()

# Define nodes (steps)
graph.add_node("web_search", search_web)
graph.add_node("finance_analysis", analyze_finance)

# Define workflow path
graph.set_entry_point("web_search")
graph.add_edge("web_search", "finance_analysis")  # Web Search → Finance

# Build the graph
workflow = graph.compile()

# Function to run workflow
def run_workflow(query, stock_symbol):
    inputs = {"query": query, "stock_symbol": stock_symbol}
    return workflow.invoke(inputs)
