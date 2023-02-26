import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)

    a_list = res.html.xpath("/html/body/main/content/ul/li[*]/div/a")

    for a in a_list[::-1]:
        url = a.attrs.get('href')
        if not url.startswith('http'):
            url = f'https:{url}'
        obj.create_task(
            unique_key=a.attrs.get('href'),
            name=a.text.strip(),
            url=url
        )

