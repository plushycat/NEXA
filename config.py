import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


LLM = ChatOpenAI(temperature=0, model_name='gpt-4', openai_api_key=OPENAI_API_KEY)
embeddings_model = OpenAIEmbeddings(model='text-embedding-3-large', openai_api_key=OPENAI_API_KEY)
