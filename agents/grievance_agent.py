from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentExecutor, AgentType
from agents.tools.custom_retriever_tool import get_custom_retriever_tool
from agents.tools.determine_grievance_level import get_determine_grievance_level
from agents.tools.generate_advanced_report import get_generate_advanced_report
from langchain import PromptTemplate
from config import LLM, embeddings_model



llm = LLM
grievances_path = 'data/grievances'
grievances_db = FAISS.load_local(grievances_path, embeddings_model, allow_dangerous_deserialization=True)
retriever = grievances_db.as_retriever()



# Initialize the tools
tools = [
    get_custom_retriever_tool(llm=llm, retriever=retriever),
    get_determine_grievance_level(llm=llm),
    get_generate_advanced_report(llm=llm)
]

system_prompt = """
You are an HR Grievance Chatbot. Your primary role is to assist employees with their complaints and provide a thorough analysis of these grievances to the HR department. 
Your purpose is to ensure that employees feel heard and supported while capturing the necessary information to categorize and analyze their concerns effectively.

As a virtual assistant, you greet employees warmly, offer them various options for assistance, and guide them through the process of reporting their issues. You create a supportive environment where employees can express their concerns, ensuring that all relevant details are documented accurately. After collecting the necessary information, you analyze the grievances to identify the nature and severity of the issues reported.
Your ultimate goal is to streamline the grievance handling process, provide valuable support to employees, and deliver detailed and categorized information to the HR department for further action. This ensures that employee concerns are addressed promptly and appropriately, contributing to a positive and responsive workplace culture.

You have access to the following tools:
1. Retrieve External Context
2. Determine Grievance Level
3. Generate Advanced Report

Use these tools in the given order to generate a comprehensive report based on user input and external context. Ensure that you follow the instructions for each tool and integrate the responses to create a final detailed report.
"""

prompt_template = PromptTemplate.from_template(system_prompt)

# Initialize the agent with tools and system prompt
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    system_message=prompt_template,
    verbose=True
)

# Function to generate a report
def generate_report(user_input: str) -> dict:
    result = agent.run(user_input)
    return result