import google.generativeai as genai
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env file from root directory
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# Access environment variables
SECRET_KEY = os.getenv('GEMINI_API')
genai.configure(api_key=SECRET_KEY)

def generate_text(text, target_lang="Hindi"):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    #prompt = f"Answer the following query concisely in 20 words in clean text: {text}"
    prompt = f"""You are a warm and polite AI voice assistant.
            Respond to the user's request in a helpful and empathetic tone. 
            Use simple words. Keep the answer under 100 words and use longer sentences.

            Query: {text}
            Response:"""
    try:
        # Generate response
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't process that request."
