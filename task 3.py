pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai

# ===== Gemini setup =====
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-pro")

# ===== Simple decision rule =====
def needs_web_search(question):
    keywords = ["who", "what", "latest", "news", "current", "update"]
    return any(word in question.lower() for word in keywords)

# ===== Web search function =====
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

# ===== Ask LLM to summarize =====
def summarize_with_llm(question, search_results):
    context = ""
    for r in search_results:
        context += f"- {r['title']}: {r['snippet']}\n"

    prompt = f"""
Question: {question}

Web search results:
{context}

Please provide a clear, concise, and accurate answer based on the information above.
"""

    response = model.generate_content(prompt)
    return response.text

# ===== Main agent logic =====
def main():
    question = input("Ask a question: ")

    if needs_web_search(question):
        print("\n[Agent] Web search required.\n")
        results = web_search(question)

        if not results:
            print("No search results found.")
            return

        summary = summarize_with_llm(question, results)
        print("\nFinal Answer:\n")
        print(summary)

    else:
        print("\n[Agent] Web search not required.\n")
        response = model.generate_content(question)
