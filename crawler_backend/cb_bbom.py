import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    for card in soup.find_all("div", {"class": "view-card__top"}):
        a = card.find("a")
        if a:
            div = card.find("div", {"class": "view-card__excerpt"})
            if div:
                data = div.text.strip()
            else:
                data = ""
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=a.text.strip(),
                url=a.attrs.get('href'),
                data=data
            )
