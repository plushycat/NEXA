# About this fork:
## This fork aims to replace the OpenAI implementation with that of HuggingFace, and much more.


# HR Chatbot

## 📋 Description

HR Chatbot is an intelligent, AI-powered chatbot designed to handle HR-related inquiries and grievances efficiently. It provides a conversational interface for employees, HR personnel, and administrators to interact with the system, receive relevant information, and submit grievances. The chatbot leverages advanced natural language processing techniques to understand user intent, collect detailed information, and generate comprehensive reports.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI Models**: OpenAI GPT-4, Gemini-Pro
- **Libraries**: LangChain, Pydantic, Google Generative AI, Pandas, OpenAI
- **Deployment**: Streamlit Cloud

## 🔧 How It Works

1. **Intent Recognition**:
   - Utilizes a pre-trained language model (OpenAI GPT-4) to classify user inquiries into general inquiries, HR or payroll questions, and grievances.
   - The intent classification is performed using structured prompts and responses, ensuring high accuracy in understanding user intent.

2. **Grievance Handling**:
   - Collects detailed information about grievances through a conversational flow.
   - Uses a structured LLM to determine if more information is needed or if the collected information is sufficient to generate a report.
   - The agent interacts with users, asking relevant follow-up questions until all necessary information is gathered.

3. **Internal and External Inquiries**:
   - Handles inquiries related to internal HR policies and external general questions.
   - Provides accurate and relevant information by querying internal and external databases using a vector store retriever.
   - The system can dynamically adapt to user queries, offering precise and context-aware responses.

4. **Interactive and Conversational**:
   - Engages users in a friendly and professional manner.
   - Ensures that users feel heard and supported throughout the interaction.
   - Utilizes conversational AI techniques to maintain a natural and engaging dialogue with users.

## 🎯 Functionalities

1. **Intent Recognition**:
   - Classifies user inquiries into categories such as general inquiries, HR or payroll questions, and grievances.
   - Provides appropriate responses based on the detected intent.

2. **Grievance Handling**:
   - Guides users through a series of questions to collect detailed information about grievances.
   - Generates comprehensive reports based on the collected information.

3. **Internal and External Inquiries**:
   - Responds to inquiries related to internal HR policies and external general questions.
   - Retrieves relevant information from internal and external sources to provide accurate answers.

4. **User Engagement**:
   - Creates a supportive environment for users to report issues and seek information.
   - Ensures that interactions are professional and empathetic.

## 🚀 Problem It Solves

HR Chatbot addresses the following challenges:

- **Efficient Grievance Handling**: Streamlines the process of reporting and analyzing grievances, ensuring timely and appropriate responses.
- **Accurate Information Delivery**: Provides precise answers to HR-related inquiries, reducing the workload on HR personnel.
- **User Engagement**: Creates a supportive environment where employees feel comfortable reporting issues and seeking information.

## 📝 How to Setup

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/your-username/hr-chatbot.git
   cd HR-Chatbot
   ```

2. Set Up the Environment:

    - Create a virtual environment:

        ```sh
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate`
        ```

    - Install dependencies:

        ```sh
        pip install -r requirements.txt
        ```
    
3. Environment Variables:

Create a .env file in the root directory and add the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_genai_key
```

4. Run the Application:

```sh
streamlit run main.py
```

## 🔄 User Flow Examples

For detailed user flow examples for all three options (general inquiries, HR or payroll questions, grievances), please refer to the [Chat Flow Examples](./chat_flow_examples.md).


