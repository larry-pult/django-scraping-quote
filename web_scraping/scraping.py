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
    for i in range(1, 11):
        quotes = scrape_quotes(i)
        for quote in quotes:
            if "quote" not in quote:
                print("no quote:", quote)
            if "author" not in quote:
                print("no author:", quote)
            if "tags" not in quote:
                print("no tags:", quote)
        print(quotes)
