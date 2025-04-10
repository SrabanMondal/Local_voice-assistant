import google.generativeai as genai

genai.configure(api_key="AIzaSyB2TvHIt8HsoiKuURmb7jme5IvF1JbBXF8")

def generate_text(text, target_lang="Hindi"):
    model = genai.GenerativeModel("gemini-2.0-flash")
    if target_lang:
        prompt = f"Respond to the following query in {target_lang}: {text}"
    else:
        prompt = f"Answer the following query concisely: {text}"

    try:
        # Generate response
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't process that request."
