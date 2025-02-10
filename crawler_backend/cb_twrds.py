import urllib

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    for item in soup.find_all("li"):
        a = item.find('a')
        if a and a.get("href") and a.text.strip():
            obj.create_task(
                unique_key=a.get('href'),
                name=a.text.strip(),
                url=a.get('href')
            )
