import os
from langchain_groq import ChatGroq
from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from tools.product_fetcher import fetch_product_data
from dotenv import load_dotenv
load_dotenv()


SYSTEM_PROMPT = """You are a Product Data Collector Agent. Your job is to gather 
detailed, structured information about a product using your tools and knowledge.

You MUST use the fetch_product_data tool to get real-world data.

Once you have enough information, return a structured report with these exact sections:
- **Product Name**: 
- **Category**: 
- **Price Range**: (e.g., ₹15,000 – ₹20,000 or $200 – $250)
- **Key Specifications**: (bullet list of 5–8 specs)
- **User Ratings**: (out of 5, with brief sentiment)
- **Availability**: (Online/Offline/Both)
- **Target Audience**: 
"""


def collect_product_data(product_name: str, groq_api_key: str = None, serpapi_key: str = None) -> str:
    """
    Uses a ReAct agent to collect structured product data.
    """
    # Set API keys in environment for tools to use
    if groq_api_key:
        os.environ["GROQ_API_KEY"] = groq_api_key
    if serpapi_key:
        os.environ["SERPAPI_KEY"] = serpapi_key

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
    )

    tools = [fetch_product_data]
    
    # Get the standard ReAct prompt from LangChain Hub
    prompt = hub.pull("hwchase17/react")

    # Create the agent
    agent = create_react_agent(llm, tools, prompt)

    # Create the executor
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )

    input_text = f"{SYSTEM_PROMPT}\n\nResearch this product: {product_name}"
    
    response = agent_executor.invoke({"input": input_text})

    return response["output"]