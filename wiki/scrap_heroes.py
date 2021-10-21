import json
from traceback import print_exc

import requests

LIST_OF_ALL_HEROES_URL = "https://heroes.thelazy.net/index.php/List_of_heroes_(HotA)"
html = requests.get(LIST_OF_ALL_HEROES_URL)

from bs4 import BeautifulSoup

soup = BeautifulSoup(html.text, 'html.parser')
table = soup.find('table')


def scrap_name(td):
    img = td.find("img")
    return img.get("alt"), {
        "hero_image": f'https://heroes.thelazy.net{img.get("src")}'
    }


def scrap_class(td):
    a = td.find("a")
    return {"class": a.text.strip()}


def scrap_specialty(td):
    a, img = td.find("a"), td.find("img")
    return {
        "specialty_img": f'https://heroes.thelazy.net{img.get("src")}',
        "specialty": a.get("title").strip()
    }


def scrap_skill(td, i):
    img = td.find("img")
    a = td.find("a")
    if not img or not a:
        return None

    return {
        f"secondary_skill_img_{i}": f'https://heroes.thelazy.net{img.get("src")}',
        f"secondary_skill_{i}": a.get("title").strip()
    }


def scrap_hero(td):
    img = td.find("img")
    span = td.find("span")
    return {
        "hero_name": span.get("title"),
        "hero_image": f'https://heroes.thelazy.net{img.get("src")}'
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


val = None
ans = {}
print(table)
try:
    for i, td in enumerate(table.find_all('td')):
        if i % 10 == 0:
            name, val = scrap_name(td)
            ans[name] = {}
        elif i % 10 == 1:
            val = scrap_class(td)
        elif i % 10 == 2:
            val = scrap_specialty(td)
        elif i % 10 == 4:
            val = scrap_skill(td, 1)
        elif i % 10 == 6:
            val = scrap_skill(td, 2)
        else:
            pass

        if val:
            ans[name].update(val)
finally:
    pass

print(ans)
print(json.dumps(ans))
