import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)

    li_list = res.html.xpath("/html/body/main/ul[*]/li")

    for li in li_list:
        a = li.find('a')
        if a:
            a = a[0]
        obj.create_task(
            unique_key=a.attrs.get('href'),
            name=li.text.strip(),
            url=a.attrs.get('href')
        )

