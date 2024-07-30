import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    for li in soup.find("div", {"class": "flex-1 min-h-0"}).find_all("li"):
        a = li.find("a")
        h2 = li.find("h2")
        p = li.find("p")
        if a and h2:
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=h2.text.strip(),
                url=a.attrs.get('href'),
                data=p.text.strip() if p else ""
            )
