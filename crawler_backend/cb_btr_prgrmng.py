import urllib

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    links = []

    selector = "#root > div > div.l.c > div > div > main > div"

    divs = res.html.find(selector, first=True)
    for div in divs.find(".l"):
        if div:
            a = div.find("a", first=True)
            if a:
                link: str = a.attrs.get("href")
                h2 = a.find("h2", first=True)

                if all([h2, link, link not in links, link.startswith("/")]):
                    title = h2.text.strip()

                    links.append(link)
                    obj.create_task(
                        unique_key=link,
                        name=title,
                        url=urllib.parse.urljoin(base_url, link)
                    )
