import json
import requests
import hashlib
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook

def main():
    with open("data.json", "r") as file:
        data = json.load(file)

    webhook_url = data["webhook_url"]

    products = data["products"]

    for prod in products:
        print(f"Checking product {prod['name']}")

        for source in prod["sources"]:
            print(f"  - Checking source {source['name']}")

            url = source["url"]
            print(f"    Fetching url {url}")
            response = requests.get(url)

            # response.content?
            soup = BeautifulSoup(response.content, "html.parser")

            for field in source["watch"]:
                print(f"      - Checking field {field}")

                elements = soup.select(field)

                if len(elements) != 1:
                    print(f"incorrect elements length: {len(elements)}")

                element = elements[0]

                value = element.text.strip()

                # print(f"        Value: {value}")

                cache_key = hashlib.md5(f"{prod['name']}{source['name']}{field}".encode()).hexdigest()

                try:
                    with open("cache.json", "r") as file:
                        cache = json.load(file)
                except FileNotFoundError:
                    print("        Info: empty cache")
                    cache = {}

                if cache_key in cache:
                    print(f"        Cache key {cache_key} found")
                    if cache[cache_key] == value:
                        print("        Cache matched - no change")
                    else:
                        print("        CACHE DIFFERENCE")
                        send_notification(webhook_url, prod["name"], source["name"], url)

                with open("cache.json", "w") as file:
                    cache[cache_key] = value

                    file.write(json.dumps(cache))

def send_notification(webhook_url, product_name, source_name, url):
    webhook = DiscordWebhook(url=webhook_url, content=f"Product {product_name} updated on source [{source_name}]({url})!")
    webhook.execute()

main()

