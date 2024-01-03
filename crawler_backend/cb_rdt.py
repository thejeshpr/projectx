import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    logging.info("Establishing connection to url")
    base_url = obj.site_conf.base_url
    res = WebClient.get(base_url)

    logging.debug(f"status code:{res.status_code}")
    logging.debug(f"response: {res.content}")

    found_links = dict()

    for p in res.html.find(".top-matter"):
        a = p.find("a", first=True)
        if a:
            link = a.attrs.get("href")
            if link not in found_links:
                li = p.find(".first", first=True)
                if li:
                    comment = li.find("a", first=True)
                    comment_link = comment.attrs.get('href')
                    comment_link = comment_link.replace("old.reddit.com", "www.reddit.com")
                    found_links[a.text.strip()] = comment_link
                    obj.create_task(
                        unique_key=comment_link,
                        name=a.text.strip(),
                        url=comment_link
                    )
