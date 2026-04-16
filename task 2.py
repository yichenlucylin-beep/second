pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup

def search_web(query):
    url = "https://duckduckgo.com/html/"
    params = {"q": query}
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for result in soup.select(".result")[:5]:
        title = result.select_one(".result__a")
        snippet = result.select_one(".result__snippet")

        if title:
            results.append({
                "title": title.get_text(),
                "url": title["href"],
                "snippet": snippet.get_text() if snippet else ""
            })

    return results


def main():
    query = input("Enter search query: ")
    results = search_web(query)

    print("\nSearch Results:\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(r["url"])
        if r["snippet"]:
            print(r["snippet"])
        print()


if __name__ == "__main__":
    main()
