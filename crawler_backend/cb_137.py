
import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    extras = json.loads(obj.site_conf.extra_data_json)
    soup = WebClient.get_bs(base_url)
    
    tab = soup.find("table", {"class":"table-list table table-responsive table-striped"})
    for tr in tab.find_all("tr")[1:]:
        a = tr.find_all("a")[1]
        if a:
            tds = tr.find_all("td")
            data = f"Size: {tds[4].text.strip()}\nSe: {tds[1].text.strip()}\nLe: {tds[2].text.strip()}"
        
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=a.text.strip(),
                url=urllib.parse.urljoin(extras["article_base_url"], a.attrs.get('href')),
                data=data
            )
