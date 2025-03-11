from agents.grievance_agent import generate_report
import pandas as pd
from transformers import pipeline
from collections import Counter
from config import LLM

# Intent Engines
from intent_engine.determine_follow_up_or_final_response import determine_follow_up_or_final_response
from intent_engine.determine_intent import determine_intent
from intent_engine.determine_option import determine_option
from intent_engine.process_navigation import process_navigation as determine_navigation

# UTILS
from utils.query_vector_store import query_vector_store
from utils.load_vector_stores import load_vector_stores
from chatbot.collect_grievance_info import collect_grievance_info

# Initialize DataFrame to store chat responses
chat_data = pd.DataFrame(columns=["Role", "Content"])

llm = LLM

# System Instructions
system_instructions = """
You are an HR Grievance Chatbot. Your primary role is to assist employees with their complaints and provide a thorough analysis of these grievances to the HR department. Your purpose is to ensure that employees feel heard and supported while capturing the necessary information to categorize and analyze their concerns effectively.

As a virtual assistant, you greet employees warmly, offer them various options for assistance, and guide them through the process of reporting their issues. You create a supportive environment where employees can express their concerns, ensuring that all relevant details are documented accurately. After collecting the necessary information, you analyze the grievances to identify the nature and severity of the issues reported.

Your ultimate goal is to streamline the grievance handling process, provide valuable support to employees, and deliver detailed and categorized information to the HR department for further action. This ensures that employee concerns are addressed promptly and appropriately, contributing to a positive and responsive workplace culture.
"""

# Messages dictionary
messages = {
    "welcome_message": "Hello! Welcome to the HR Grievance Chatbot. May I have your name, please?",
    "greet_user": "Nice to meet you, {username}! How is your day going? What issue is bothering you? I am here to help you make your day better. Thank you for visiting. How can I assist you today? Please choose an option:\n1. General Inquiry\n2. HR or Payroll Questions\n3. Capture and Analyze Grievances",
    "capture_details": "You've selected to capture and analyze a grievance. Let's start with the details. Where did the incident happen?",
    "general_inquiry": "Sure, let's handle your general inquiry. What would you like to know?",
    "hr_payroll_question": "Sure, let's handle your HR or payroll question. What would you like to ask?",
    "ask_date_time": "Thank you for sharing that. When did the incident happen? Please provide the date and time.",
    "ask_description": "Got it. Please describe exactly what happened.",
    "ask_involved": "Thank you for the description. Who was involved? Please list all people involved (victims, witnesses).",
    "ask_feelings": "I appreciate that information. How did the situation make you feel? (e.g., anger, sadness)",
    "ask_concerns": "Thank you for sharing your feelings. Do you have any specific concerns (e.g., discrimination, physical or emotional violence, safety issues)?",
    "ask_danger": "Was anyone in danger? Describe any injuries or violent actions.",
    "ask_urgency": "Thank you for providing these details. Based on what you've shared, how urgent do you feel this issue is?",
    "ask_action": "What would you like to do about it?",
    "ask_additional_details": "Is there anything else you would like to share about this incident?",
    "ask_next_option": "Does this answer your question or would you like to add more detail?",
    "return_to_main_menu": "Sure, we're back at the main menu. How can I assist you further? Please choose an option:\n1. General Inquiry\n2. HR or Payroll Questions\n3. Capture and Analyze Grievances",
    "end_chat": "Thank you for using the HR Grievance Chatbot. If you need further assistance, please let us know.",
    "invalid_option": "I'm sorry, I didn't understand that. Please choose a valid option:\n1. General Inquiry\n2. HR or Payroll Questions\n3. Capture and Analyze Grievances"
}

def process_message(user_input, chat_history, context, grievance_stage, llm, prompt):
    global chat_data
    global username
    global final_report
    global admin_recommendations
    global intent

    is_return, is_query = determine_navigation(user_input)

    if is_return:
        response_text = messages["return_to_main_menu"]
        grievance_stage = 2  # Return to the main options
    else:
        if grievance_stage == 0:
            response_text = messages["welcome_message"]
            grievance_stage = 1

        elif grievance_stage == 1:
            username = user_input.strip()
            response_text = messages["greet_user"].format(username=username)
            grievance_stage = 2

        elif grievance_stage == 2:
            intent = determine_intent(user_input)
            option_number = determine_option(user_input=user_input)
            if option_number == 3:
                response_text = "You've selected to capture and analyze a grievance. Let's start with the details. Please describe the incident in detail."
                grievance_stage = 3
            elif option_number == 1:
                response_text = messages["general_inquiry"]
                grievance_stage = 14  # Set to a different stage for handling general inquiries
            elif option_number == 2:
                response_text = messages["hr_payroll_question"]
                grievance_stage = 20  # Set to a different stage for handling HR or Payroll questions
            else:
                response_text = messages["invalid_option"]

        elif grievance_stage == 3:
            context += f"\n{user_input}"
            response = collect_grievance_info(context)
            if response.is_complete:
                report = generate_report(response.collected_info)
                response_text = report + f"\n\n{messages['ask_next_option']}"
                grievance_stage = 13  # New stage to ask if the user wants to return to the main menu
            else:
                response_text = response.next_question
                grievance_stage = 3  # Stay in the same stage to continue collecting information

        elif grievance_stage == 13:
            if user_input.lower() in ["yes", "y"]:
                response_text = messages["greet_user"].format(username=username)
                grievance_stage = 2  # Return to the main options
            else:
                response_text = messages["end_chat"]
                grievance_stage = 0  # End the chat

        elif grievance_stage == 14:  # Handle General Inquiry similar to Option 2
            context += f"\nGeneral Inquiry: {user_input}"
            response_text = f"{query_vector_store(intent, user_input, llm, prompt)}\n\n{messages['ask_next_option']}"  # This will be the final response
            grievance_stage = 14  # Stay in the same stage to allow more general inquiries

        elif grievance_stage == 15:
            context += f"\nGeneral Inquiry Follow-Up: {user_input}"
            response_text = f"{query_vector_store(intent, user_input, llm, prompt)}\n\n{messages['ask_next_option']}"  # This will be the final response
            grievance_stage = 14  # Stay in the same stage to allow more general inquiries

        elif grievance_stage == 20:  # Handle HR or Payroll Questions
            context += f"\nHR or Payroll Question: {user_input}"
            response_text = f"{query_vector_store(intent, user_input, llm, prompt)}\n\n{messages['ask_next_option']}"  # This will be the final response
            grievance_stage = 20  # Stay in the same stage to allow more HR or payroll questions

        elif grievance_stage == 21:
            context += f"\nHR or Payroll Follow-Up: {user_input}"
            response_text = f"{query_vector_store(intent, user_input, llm, prompt)}\n\n{messages['ask_next_option']}"  # This will be the final response
            grievance_stage = 20  # Stay in the same stage to allow more HR or payroll questions
            
    chat_data = chat_data.append({"Role": "User", "Content": user_input}, ignore_index=True)
    chat_data = chat_data.append({"Role": "Bot", "Content": response_text}, ignore_index=True)
    return response_text, grievance_stage, context