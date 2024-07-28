from langchain.tools import tool
from langchain import LLMChain, PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

def get_custom_retriever_tool(llm, retriever):
    @tool("Custom_Retriever_Tool")
    def custom_retriever_tool(input_data: str) -> str:
        """Fetch external context based on user input with tailored instructions for the use case."""
        template = """
        You are an HR assistant tasked with retrieving relevant external context based on employee grievances. The context provided will be used to better understand the issues faced by employees and to determine the level of grievance. Please ensure the context is accurate, comprehensive, and relevant to the employee's complaint.

        Context: {context}

        Question: {input_details}
        """
        prompt = ChatPromptTemplate.from_template(template)
        def format_docs(docs):
            return "\n\n".join([d.page_content for d in docs])


        chain = (
            {"context": retriever | format_docs, "input_details": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        # Invoke the chain with the provided input_data
        result = chain.invoke(input_data)
        return result
    
    return custom_retriever_tool