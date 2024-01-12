import requests
import random
from bs4 import BeautifulSoup as bs

@hell_cmd(pattern="hq")
async def hurray(e):
    url = "https://www.brainyquote.com/topics/hackers-quotes"

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = bs(response.content, "html.parser", from_encoding="utf-8")
        quotes = soup.find_all("div", "clearfix")

        if quotes:
            selected_quote = random.choice(quotes)
            quote_text = selected_quote.findNext().text
            quote_author = selected_quote.findNext().findNext().text

            message = f"{quote_text}\n\n**{quote_author}**"
            await eor(e, message)
        else:
            await eor(e, "No quotes found at the moment.")
    except requests.exceptions.RequestException as err:
        await eor(e, f"Error fetching quotes: {err}")

CmdHelp("hq").add_command(
    "hq", "This command gives you a random hacker quote."
).add()
