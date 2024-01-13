import json
import urllib.request
import os

apikey = os.environ.get("GNEWS_API_KEY")
url = f'https://gnews.io/api/v4/search?q="conspiracy"&lang=en&country=us&max=10&apikey={apikey}'

with urllib.request.urlopen(url) as response:
    data = json.loads(response.read().decode("utf-8"))
    articles = data["articles"]

    for i in range(len(articles)):
        # articles[i].title
        print(f"Title: {articles[i]['title']}")
        print(f"Date: {articles[i]['publishedAt']}")
        # articles[i].description
        # print(f"Description: {articles[i]['description']}")
        # You can replace {property} below with any of the article properties returned by the API.
        # articles[i].{property}
        # print(f"{articles[i]['{property}']}")

        # Delete this line to display all the articles returned by the request. Currently only the first article is displayed.
        # break
