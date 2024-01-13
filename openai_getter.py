import openai
import json
import requests
import os
from datetime import datetime

GNEWS_API_KEY = os.environ.get("GNEWS_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

TODAY = datetime.today().strftime("%Y%m%d")

NEWS_CATEGORIES = [
    "general",
    "world",
    "nation",
    "business",
    "technology",
    "entertainment",
    "sports",
    "science",
    "health",
]


def query_GPT(prompt: str):
    messages = [{"role": "user", "content": prompt}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613", messages=messages
    )
    response_message = response["choices"][0]["message"]["content"]

    return response_message


def get_todays_headlines():
    today = TODAY
    os.mkdir(f"headlines/{today}")
    for category in NEWS_CATEGORIES:
        res = requests.get(
            f"https://gnews.io/api/v4/top-headlines?category={category}&lang=en&country=us&apikey={GNEWS_API_KEY}"
        )
        with open(f"headlines/{today}/{category}.json", "w") as outfile:
            outfile.write(json.dumps(res.json()))
        if category == "nation":
            headlines = res.json()
    return headlines


def create_GPT_prompt(prompt, headlines) -> str:
    """Generate the news prompt to be fed to GPT model"""
    for headline in headlines:
        prompt += f'  \n"{headline}"'
    return prompt


def parse_headline_response(res: dict) -> list[str]:
    articles = res["articles"]
    return [article["title"] for article in articles]


def write_result(prompt, result):
    output = "## Prompt:\n\n" + prompt + "\n\n" + "## Response:\n\n" + result
    output += "\n--------------------------------------------------------\n\n"

    with open("outputs.md", "a") as outfile:
        outfile.write(output)
    return output


def main():
    prompt1 = f"Create a fictional 3 paragraph government report about a political conspiracy theory combining the following:\n"
    prompt2 = f"Find some common themes in the following headlines:\n"

    prompt = prompt2
    # headlines = get_todays_headlines()

    with open(f"headlines/{TODAY}/nation.json", "r") as res_file:
        headlines = parse_headline_response(json.loads(res_file.read()))

    full_prompt = create_GPT_prompt(prompt, headlines)
    res = query_GPT(full_prompt)
    print(write_result(full_prompt, res))


if __name__ == "__main__":
    main()
