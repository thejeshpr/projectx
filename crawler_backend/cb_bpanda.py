import json
from urllib.parse import urlparse, urljoin
from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    extras = json.loads(obj.site_conf.extra_data_json)
    cat = extras.get("category", "")
    typ = extras.get("type", "")
    url = obj.site_conf.base_url.format(category=cat, type=typ)

    soup = WebClient.get_bs(url)
    section = soup.find("section")
    if section:

        for a in section.find_all("a", {"class": "title post-link"}):
            link = a.attrs.get("href").split("?")[0]
            name = a.text.strip()
            obj.create_task(
                unique_key=link,
                name=name,
                url=link
                # data=data
            )
