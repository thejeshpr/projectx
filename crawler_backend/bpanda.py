import json
from urllib.parse import urlparse, urljoin
from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    extras = json.loads(obj.site_conf.extra_data_json)
    cat = extras.get("category", "")
    typ = extras.get("type", "")
    url = obj.site_conf.base_url.format(category=cat, type=typ)

    res = WebClient.get(url)
    # links = res.html.xpath("/html/body/main/section/article[*]/h2/a")

    section = res.html.find("section")
    if section:
        section = section[0]

        for intro_div, header in zip(section.find('div.intro'), section.find('header')):
            a = header.find('a')[0]
            link = a.attrs.get("href").split("?")[0]
            name = a.attrs.get("title").replace("Permanent Link to ", "")

            obj.create_task(
                unique_key=link,
                name=name,
                url=link,
                data=intro_div.find('p', first=True).text
            )
