import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    
    divs = soup.find_all("div", {"class":"post"})
    for div in divs:
        a = div.find("a")
        if a:
            story_div = div.find("div", {"class":"storycontent"})
            content = story_div.text.strip() if story_div else ""
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=a.text.strip(),
                url=a.attrs.get('href'),
                data=content
            )
