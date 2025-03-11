from transformers import pipeline
from config import LLM

class GrievanceInfoCollector:
    def __init__(self, llm):
        self.llm = llm
        self.collected_info = {}
        self.is_complete = False
        self.next_question = "Where did the incident happen?"

    def collect_info(self, user_input):
        if "incident_location" not in self.collected_info:
            self.collected_info["incident_location"] = user_input
            self.next_question = "When did the incident happen? Please provide the date and time."
        elif "incident_date_time" not in self.collected_info:
            self.collected_info["incident_date_time"] = user_input
            self.next_question = "Please describe exactly what happened."
        elif "incident_description" not in self.collected_info:
            self.collected_info["incident_description"] = user_input
            self.next_question = "Who was involved? Please list all people involved (victims, witnesses)."
        elif "people_involved" not in self.collected_info:
            self.collected_info["people_involved"] = user_input
            self.next_question = "How did the situation make you feel? (e.g., anger, sadness)"
        elif "feelings" not in self.collected_info:
            self.collected_info["feelings"] = user_input
            self.next_question = "Do you have any specific concerns (e.g., discrimination, physical or emotional violence, safety issues)?"
        elif "specific_concerns" not in self.collected_info:
            self.collected_info["specific_concerns"] = user_input
            self.next_question = "Was anyone in danger? Describe any injuries or violent actions."
        elif "danger" not in self.collected_info:
            self.collected_info["danger"] = user_input
            self.next_question = "Based on what you've shared, how urgent do you feel this issue is?"
        elif "urgency" not in self.collected_info:
            self.collected_info["urgency"] = user_input
            self.next_question = "What would you like to do about it?"
        elif "action" not in self.collected_info:
            self.collected_info["action"] = user_input
            self.next_question = "Is there anything else you would like to share about this incident?"
        elif "additional_details" not in self.collected_info:
            self.collected_info["additional_details"] = user_input
            self.is_complete = True
            self.next_question = "Thank you for providing all the details. We will now generate a report."

        return self

def collect_grievance_info(context):
    collector = GrievanceInfoCollector(LLM)
    collector.collect_info(context)
    return collector