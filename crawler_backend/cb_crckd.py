import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    
    articles = soup.find_all("article")
    for article in articles:
        a = article.find("a")
        if a:
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=a.attrs.get('title'),
                url=a.attrs.get('href')
            )
