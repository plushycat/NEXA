from langchain.tools import tool
from langchain import LLMChain, PromptTemplate

def get_determine_grievance_level(llm):
    
    # Determine_Grievance_Level Tool
    @tool("Determine_Grievance_Level")
    def determine_grievance_level(context: str) -> str:
        """Determine the level of the grievance based on the provided context and guide the sequence of actions."""
        prompt_template = PromptTemplate.from_template(
            """
            Based on the provided context, determine the level of the grievance and specify the subsequent actions.
            Context: {context}
            
            Levels:
            Level 1:
            - Minor incidents commonly addressed by first-line management.
            - Examples: Performance inquiry, Safety hazard inquiry, Pay inquiry, etc.
            - Response time: within a given work week.

            Level 2:
            - Detected through language aggressiveness and require attention within 3 to 7 days of the incident.
            - Examples: Performance Change reporting, Discrimination reporting, Compliance reporting, etc.
            - Response time: within 3 to 7 days.

            Level 3:
            - Detected through language aggressiveness and/or includes minor physical injury.
            - Requires immediate attention.
            - Examples: Minor Safety incident, Discrimination complaints, Jobsite Violence Complaints, etc.
            - Response time: immediate internal resolution.

            Level 4:
            - Detected through language aggressiveness and/or includes minor to severe physical injury through violence.
            - Requires immediate attention and is reported to C-Suite.
            - Examples: Major Safety accident, Discrimination with violence, Jobsite Violence, etc.
            - Response time: immediate/urgent resolution.
            """
        )
        chain = LLMChain(llm=llm, prompt=prompt_template)
        level = chain.run(context=context)
        return level
    
    return determine_grievance_level