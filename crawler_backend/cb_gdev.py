import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)

    a_list = res.html.xpath("/html/body/div[*]/div/div/div[*]/div[*]/div[*]/a")

    for a in a_list[::-1]:
        if a.attrs.get('aria-label'):
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=a.attrs.get('aria-label'),
                url=a.attrs.get('href')
            )

