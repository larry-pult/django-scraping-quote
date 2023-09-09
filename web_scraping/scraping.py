import requests
from bs4 import BeautifulSoup


def scrape_quotes(page=1):
    url = f"https://quotes.toscrape.com/page/{page}/"

    response = requests.get(url)

    if response.status_code != 200:
        return []

    # print(response.text)

    soup = BeautifulSoup(response.text, "html.parser")

    quotes = soup.find_all(class_="quote")

    quote_list = list()

    for quote_element in quotes:
        quote = quote_element.find(class_="text").text
        author = quote_element.find(class_="author").text
        tags = quote_element.find_all(class_="tag")

        quote_list.append({
            "quote": quote,
            "author": author,
            "tags": [tag.text for tag in tags]
        })

    return quote_list


if __name__ == "__main__":
    quotes = scrape_quotes(1)
    print(quotes)
