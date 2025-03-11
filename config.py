import os
from dotenv import load_dotenv
from transformers import pipeline, AutoModelForSeq2SeqLM, AutoTokenizer

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

# Load HuggingFace models
model_name = "facebook/bart-large-cnn"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
LLM = pipeline("text2text-generation", model=model, tokenizer=tokenizer)