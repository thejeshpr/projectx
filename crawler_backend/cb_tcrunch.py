import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    for item in soup.find_all('h3', {'class': 'loop-card__title'}):
        a = item.find("a")
        if a and a.text.strip() and a.attrs.get("href"):
            url = a.attrs.get('href')
            obj.create_task(
                unique_key=url,
                name=a.text.strip(),
                url=url
            )

