from langchain.tools import tool
from transformers import pipeline

def get_custom_retriever_tool(llm, retriever):
    @tool("Custom_Retriever_Tool")
    def custom_retriever_tool(input_data: str) -> str:
        """Fetch external context based on user input with tailored instructions for the use case."""
        template = """
        You are an HR assistant tasked with retrieving relevant external context based on employee grievances. The context provided will be used to better understand the issues faced by employees and to determine the level of grievance. Please ensure the context is accurate, comprehensive, and relevant to the employee's complaint.

        Context: {context}

        Question: {input_details}
        """
        prompt = template.format(context=retriever, input_details=input_data)
        result = llm(prompt)
        return result[0]['generated_text']
    
    return custom_retriever_tool