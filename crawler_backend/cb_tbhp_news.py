import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)
    article_base_url = extras.get("base_url", "")

    li_list = res.html.xpath('//*[@id="newslist"]/li[*]/div/div[2]/h2/a')

    for li in li_list[::-1]:
        a = li.find('a', first=True)
        url = urllib.parse.urljoin(article_base_url, a.attrs.get('href'))

        obj.create_task(
            unique_key=url,
            name=a.attrs.get('title').strip(),
            url=url
        )

