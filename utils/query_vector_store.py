# src/intent_engine/query_vector_store.py
from utils.load_vector_stores import load_vector_stores
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY


# Load vector stores
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-large', openai_api_key=OPENAI_API_KEY)
internal_path = 'data/internal_policy'
external_path = 'data/external_policy'
grievances_path = 'data/grievances'
external_policy_db, internal_policy_db, grievances_db = load_vector_stores(
    internal_path=internal_path,
    external_path=external_path,
    grievances_path=grievances_path,
    embeddings_model=embeddings_model
)

def query_vector_store(intent, user_input, llm, tools_prompt):
    if intent == "External":
        retriever = external_policy_db.as_retriever()
    elif intent == "Internal":
        retriever = internal_policy_db.as_retriever()
    elif intent == "Grievances":
        retriever = grievances_db.as_retriever()
    else:
        return "Sorry, I couldn't classify your query. Please try again."

    tool = create_retriever_tool(
        retriever,
        f"search_{intent.lower()}",
        f"Searches and returns excerpts from the knowledge base for {intent}."
    )

    tools = [tool]
    agent = create_openai_tools_agent(llm, tools, tools_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    result = agent_executor.invoke({"input": user_input})
    return result['output']
