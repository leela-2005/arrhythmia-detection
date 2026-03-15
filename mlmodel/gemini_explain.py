import google.generativeai as genai

# Configure Gemini API with the given key
genai.configure(api_key="your api key")

def generate_gemini_explanation(feature_contributions, prediction):
    """
    Takes SHAP feature contributions and generates a natural language clinical explanation using Gemini.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        prompt = (f"You are an AI cardiologist assistant. An ECG model just predicted '{prediction}'. "
                  f"The SHAP feature contributions that led to this prediction are: {feature_contributions}. "
                  "Please provide a simple human-readable clinical explanation describing which features influenced this prediction and why. "
                  "Your response MUST be exactly 3 lines of text. "
                  "Avoid using markdown like bold text.")
        
        response = model.generate_content(prompt)
        
        if response and response.text:
            return response.text.strip().replace('**', '').replace('__', '')
        return None
    except Exception as e:
        print(f"Gemini AI Explanation failed: {e}")
        return None
