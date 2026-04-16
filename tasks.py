pip install google-generativeai

import google.generativeai as genai

# 設定 API key
genai.configure(api_key="YOUR_API_KEY_HERE")

def main():
    model = genai.GenerativeModel("gemini-pro")

    user_question = input("Please enter your question: ")

    response = model.generate_content(user_question)

    print("\nAI Response:")
    print(response.text)

if __name__ == "__main__":
    main()
``
