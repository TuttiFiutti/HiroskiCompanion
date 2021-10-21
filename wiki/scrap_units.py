import json

import requests

LIST_OF_ALL_CREATURES_URL = (
    "https://heroes.thelazy.net/index.php/List_of_creatures_(HotA)"
)
html = requests.get(LIST_OF_ALL_CREATURES_URL)

from bs4 import BeautifulSoup

soup = BeautifulSoup(html.text, "html.parser")
table = soup.find("table")


def scrap_name(td):
    img = td.find("img")
    return (
        img.get("alt"),
        {"creature_image": f'https://heroes.thelazy.net/{img.get("src")}'},
    )


def scrap_town(td):
    img = td.find("img")
    span = td.find("span")
    return {
        "town": span.get("title"),
        "town_image": f'https://heroes.thelazy.net/{img.get("src")}',
    }


def scrap_span(td):
    span = td.find("span")
    return {span.get("title"): span.text.strip()}


def scrap_gold(td):
    return {"Gold": td.text.strip()}


def scrap_resources(td):
    try:
        return None
    except Exception as e:
        print(e)
        return None


def scrap_extra(td):
    return {"Extra": td.text.strip()}


ans = {}
try:
    for tr in table.find_all("tr"):
        name = None
        for i, td in enumerate(tr.find_all("td")):
            if i == 0:
                name, val = scrap_name(td)
                ans[name] = {}
            elif i == 1:
                val = scrap_town(td)
            elif i == 11:
                val = scrap_gold(td)
            elif i == 12:
                val = scrap_resources(td)
            elif i == 13:
                val = scrap_extra(td)
            else:
                val = scrap_span(td)

            if val:
                print(f"{val=}")
                ans[name].update(val)
except Exception as e:
    print(e)
print(ans)
print(json.dumps(ans))
