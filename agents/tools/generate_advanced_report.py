from langchain.tools import tool
from langchain import LLMChain, PromptTemplate



def get_generate_advanced_report(llm):
    
    @tool("Generate_Advanced_Report")
    def generate_advanced_report(context: str) -> str:
        """Generate a comprehensive final report based on the given context and the determined level of grievance."""
        prompt_template = PromptTemplate.from_template(
            """
            Generate a comprehensive and professional report based on the following details:
            Context: {context}
            
            Instructions for different levels:
            
            Level 1:
            - Provide words of encouragement about the issue.
            - Provide resources to improve.
            - Policy explanations about the command structure.
            - Unresolved incidents are moved up to Level 2 resolutions.
            - Common Level 1 incidents fall within the segments of Performance, Safety, Travel, and Culture.
            - Response time: within a given work week.

            Level 2:
            - Detected through language aggressiveness and require attention within 3 to 7 days of the incident.
            - Provide the same discourse with the employee as in Level 1.
            - Send hints and reminders to management about best practices.
            - Assign an HR Specialist to assist with a resolution.
            - Common Level 2 incidents fall within the segments of Performance, Safety, Travel, Discrimination, Drugs, Compliance, and Culture.
            - Response time: within 3 to 7 days.

            Level 3:
            - Detected through language aggressiveness and/or includes minor physical injury.
            - Requires immediate attention.
            - Report to Upper Management.
            - Collect additional information to perform advisory.
            - Formal reporting procedures for all appropriate authorities.
            - Instructions and resources to both employees and leaders.
            - Help messages to decision makers for immediate resolution.
            - Common Level 3 incidents fall within the segments of Performance, Safety, Travel, Discrimination, Drugs, Compliance, Sexual Harassment, Jobsite Violence, and Culture.
            - Response time: immediate internal resolution.

            Level 4:
            - Detected through language aggressiveness and/or includes minor to severe physical injury through violence.
            - Requires immediate attention and is reported to C-Suite.
            - Formal reporting procedures for all appropriate authorities.
            - Information gathering from victims, witnesses, and leadership.
            - Instructions and resources to employees and 3rd party leaders (healthcare professionals, public authorities, Legal Professional, Not-for-Profit Leaders).
            - Help messages to decision makers for immediate resolution.
            - Common Level 4 incidents fall within the segments of Performance, Safety, Discrimination, Drugs, Sexual Harassment, Jobsite Violence, and Healthcare.
            - Response time: immediate/urgent resolution.

            The report should include the following sections:
            1. Summary of the incident
            2. Date, time, and location of the incident
            3. Detailed description of the incident
            4. People involved (victims, witnesses, aggressors)
            5. Analysis of how the situation made the employee feel
            6. Screening for violence and immediate danger
            7. Categorization of the grievance
            8. Recommendations for the employee (advice, directory, relevant authorities)
            9. Follow-up actions and response time(Imprtant)
            10. Final recommendations and next steps

            Ensure the report is written professionally and addresses all necessary details to support the employee and provide a thorough analysis for HR.
            """
        )
        
        chain = LLMChain(llm=llm, prompt=prompt_template)
        final_report = chain.run(context=context)
        return final_report
    
    return generate_advanced_report