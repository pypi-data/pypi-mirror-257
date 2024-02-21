import json
import os
import urllib3
from concurrent.futures import ThreadPoolExecutor


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

data_dir = os.path.dirname(__file__)


def check_file() -> bool:
    check: list[bool] = []
    for name in url_source:
        file_path = os.path.join(data_dir, f"{name}.json")
        if os.path.isfile(file_path) is False:
            check.append(False)
    return all(check)


def download_json_data():
    if check_file() is False:
        print("Colors database file not exist.\n Download data:")
        http = urllib3.PoolManager()

        def download_file(file_name):
            print(f"Download {file_name}.json...")
            file_path = os.path.join(data_dir, f"{file_name}.json")
            with open(file_path, "w") as file:
                url = f"https://api.color.pizza/v1/?list={file_name}"
                response = http.request("GET", url)
                json.dump(response.json(), file)

        with ThreadPoolExecutor() as executor:
            executor.map(download_file, url_source)
