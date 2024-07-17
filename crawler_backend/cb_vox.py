import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    s = set()
    for i, a in enumerate(soup.find_all('a', {"class": "qcd9z1"}), 1):
        if a and a.text not in s:
            s.add(a.text)
            obj.create_task(
                unique_key=a.get("href"),
                name=a.text.strip(),
                url=urllib.parse.urljoin(base_url, a.get("href"))
            )
