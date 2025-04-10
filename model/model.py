import google.generativeai as genai

genai.configure(api_key="AIzaSyB2TvHIt8HsoiKuURmb7jme5IvF1JbBXF8")

def generate_text(text, target_lang="Hindi"):
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = f"Answer the following query concisely in 20 words in clean text: {text}"

    try:
        # Generate response
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't process that request."
