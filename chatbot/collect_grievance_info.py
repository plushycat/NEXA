from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config import LLM

class GrievanceResponse(BaseModel):
    is_complete: bool = Field(description="Indicates whether the information collected is complete.")
    next_question: str = Field(description="The next question to ask the user for collecting more information.")
    collected_info: str = Field(description="Collected information from the user so far.")

structured_llm = LLM.with_structured_output(GrievanceResponse)

def collect_grievance_info(user_input: str) -> GrievanceResponse:
    prompt_template = f"""
    You are an HR assistant tasked with collecting detailed information about an incident from an employee. Your goal is to gather all necessary details in a friendly and supportive manner, ensuring the employee feels heard and supported. Please avoid asking the same question multiple times and adapt based on the employee's responses.

    User Input: {user_input}
    
    PLEASE COMMUNICATE WITH USER IN A FRIENDLY MANNER.

    Task: Based on the context and user input, determine if the information collected is sufficient to generate a detailed incident report. 
    If the information is complete, respond with is_complete as true and provide a summary of the collected information.
    If the information is not complete, respond with is_complete as false and provide the next question to ask the user to gather the required information.

    Ensure the collected information includes:
    - Description: Describe exactly what happened.
    - Location: Where did it happen?
    - Date and Time: When did it happen?
    - Who was involved (list all people involved - victims, witnesses).
    - How did the situation make you feel? (anger, sadness, etc.).
    - Was anyone in danger? Describe any injuries or violent actions.

    Response Format:
    {{
        "is_complete": true/false,
        "next_question": "string",
        "collected_info": "string"
    }}
    """
    structured_response = structured_llm.invoke(prompt_template)
    return structured_response