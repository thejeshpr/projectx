import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    for h2 in soup.find_all("h2", {"class": "story"}):
        a = h2.find("a")
        smry_tag = h2.findParent().find_next_sibling()
        data = smry_tag.text.strip() if smry_tag else ""
        obj.create_task(
            unique_key=a.attrs.get('href'),
            name=a.text.strip(),
            url=urllib.parse.urljoin("https:", a.attrs.get('href')),
            data=data
        )

