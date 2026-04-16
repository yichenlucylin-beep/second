import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# ===== Gemini setup =====
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-pro")

def needs_web_search(question):
    keywords = ["who", "what", "latest", "news", "current", "update"]
    return any(word in question.lower() for word in keywords)

def web_search(query):
    url = "https://duckduckgo.com/html/"
    params = {"q": query}
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for r in soup.select(".result")[:5]:
        title = r.select_one(".result__a")
        snippet = r.select_one(".result__snippet")
        if title:
            results.append({
                "title": title.get_text(),
                "url": title["href"],
                "snippet": snippet.get_text() if snippet else ""
            })
    return results

def summarize_with_llm(question, results):
    context = ""
    for r in results:
        context += f"- {r['title']}: {r['snippet']}\n"

    prompt = f"""
User Question:
{question}

Web Search Results:
{context}

Please provide a clear and concise answer based on the information above.
"""

    response = model.generate_content(prompt)
    return response.text

def main():
    print("=== Smart Research Bot ===")
    print("Ask a question and the bot will decide whether to search the web.\n")

    question = input("Your question: ")

    if needs_web_search(question):
        print("\n[Bot] Web search is required. Searching...\n")
        results = web_search(question)

        if not results:
            print("[Bot] No relevant search results found.")
            return

        answer = summarize_with_llm(question, results)
    else:
        print("\n[Bot] Web search not required. Answering directly...\n")
        answer = model.generate_content(question).text

    print("=== Final Answer ===")
    print(answer)

if __name__ == "__main__":
    main()
``
