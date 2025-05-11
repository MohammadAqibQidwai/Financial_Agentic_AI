from phi.agent import Agent
import phi.api
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
import os
import phi
from phi.playground import Playground, serve_playground_app  # FastAPI

load_dotenv()

phi.api = os.getenv("PHI_API_KEY")

# Basic web search agent
web_search_agent = Agent(
    name="web search agent",
    role="Search the web for information",
    model=Groq(id="Deepseek-R1-Distill-Qwen-32b"),
    tools=[DuckDuckGo()],
    instructions=["always include sources", "find the latest news", "find the latest tweets"],
    show_tool_calls=False,
    markdown=True,
)

# Financial agent - fetches real-time stock data and news
finance_agent = Agent(
    name="finance AI Agent",
    model=Groq(id="Deepseek-R1-Distill-Qwen-32b"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True, company_news=True, historical_prices=True, technical_indicators=True)],
    instructions=[
        "use tables for data",
        "never give code in response",
        "make response user friendly",
        "Never show the function calls in the output",
        "never show any code in output"
    ],
    show_tool_calls=False,
    markdown=True,
)

# Create and serve the app without Redis caching
app = Playground(agents=[finance_agent, web_search_agent]).get_app()

if __name__ == "__main__":
    serve_playground_app("playground:app", reload=True)
