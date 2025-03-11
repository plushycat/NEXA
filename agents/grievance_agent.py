from transformers import pipeline
from config import LLM

def generate_report(collected_info):
    prompt_template = """
    Generate a comprehensive and professional report based on the following details:
    Incident Location: {incident_location}
    Incident Date and Time: {incident_date_time}
    Incident Description: {incident_description}
    People Involved: {people_involved}
    Feelings: {feelings}
    Specific Concerns: {specific_concerns}
    Danger: {danger}
    Urgency: {urgency}
    Action: {action}
    Additional Details: {additional_details}

    The report should include the following sections:
    1. Summary of the incident
    2. Date, time, and location of the incident
    3. Detailed description of the incident
    4. People involved (victims, witnesses, aggressors)
    5. Analysis of how the situation made the employee feel
    6. Screening for violence and immediate danger
    7. Categorization of the grievance
    8. Recommendations for the employee (advice, directory, relevant authorities)
    9. Follow-up actions and response time
    10. Final recommendations and next steps

    Ensure the report is written professionally and addresses all necessary details to support the employee and provide a thorough analysis for HR.
    """
    prompt = prompt_template.format(
        incident_location=collected_info.get("incident_location", ""),
        incident_date_time=collected_info.get("incident_date_time", ""),
        incident_description=collected_info.get("incident_description", ""),
        people_involved=collected_info.get("people_involved", ""),
        feelings=collected_info.get("feelings", ""),
        specific_concerns=collected_info.get("specific_concerns", ""),
        danger=collected_info.get("danger", ""),
        urgency=collected_info.get("urgency", ""),
        action=collected_info.get("action", ""),
        additional_details=collected_info.get("additional_details", "")
    )

    result = LLM(prompt)
    return result[0]['generated_text']