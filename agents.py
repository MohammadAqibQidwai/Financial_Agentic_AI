import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools

# Load API keys from .env
load_dotenv()
GROQ_API_KEY = os.getenv(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

# Define Web Search Agent
web_search_agent = Agent(
    name="Web Search Agent",
    role="Find the latest information from the web",
    model=Groq(api_key=GROQ_API_KEY, id="mixtral"),
    tools=[DuckDuckGo()],
    instructions=[
        "Always include sources.",
        "Find the latest news and information.",
        "Provide concise and accurate results."
    ],
    show_tool_calls=False,
    markdown=True,
)

# Define Finance AI Agent
finance_agent = Agent(
    name="Finance AI Agent",
    role="Analyze stock market trends and company financials.",
    model=Groq(api_key=GROQ_API_KEY, id="mixtral"),
    tools=[YFinanceTools(
        stock_price=True,
        analyst_recommendations=True,
        stock_fundamentals=True,
        company_news=True,
        historical_prices=True,
        technical_indicators=True
    )],
    instructions=[
        "Use tables for data.",
        "Never show function calls in output.",
        "Make responses user-friendly."
    ],
    show_tool_calls=False,
    markdown=True,
)

# Export agents
agents = {
    "web_search": web_search_agent,
    "finance": finance_agent
}
