import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)

    li_list = res.html.xpath("/html/body/div[2]/div[2]/div[1]/div[1]/div[3]/div[1]/div/div[2]/div/div/div/div/div/div/div/div/div/div[2]/div/ul/li[*]/div/div[2]/h2/a")

    for li in li_list:
        a = li.find('a', first=True)

        obj.create_task(
            unique_key=a.attrs.get('href'),
            name=a.attrs.get('title').strip(),
            url=a.attrs.get('href')
        )

