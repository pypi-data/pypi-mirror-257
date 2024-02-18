import urllib3
import json
import os


url_source = [
    "default",
    "bestOf",
    "wikipedia",
    "french",
    "spanish",
    "german",
    "ridgway",
    "risograph",
    "basic",
    "chineseTraditional",
    "html",
    "japaneseTraditional",
    "leCorbusier",
    "nbsIscc",
    "ntc",
    "osxcrayons",
    "ral",
    "sanzoWadaI",
    "thesaurus",
    "werner",
    "windows",
    "x11",
    "xkcd",
]

output_path = os.path.dirname(__file__)

http = urllib3.PoolManager()

for url in url_source:
    with http.request(
        "GET", f"https://api.color.pizza/v1/?list={url}", preload_content=False
    ) as r:
        data = r.read().decode("utf-8")

    with open(f"{output_path}\\{url}.json", "w") as f:
        json.dump(json.loads(data), f)
