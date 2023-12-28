import json
import urllib

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    articles = soup.find_all('article')

    for article in articles:
        h2 = article.find('h2')
        if h2:
            title = h2.find('a').text.strip()
            a = article.find_all('a')[1]
            title = f"[{title}] - {a.text.strip()}"
            url = a.get('href')
        else:
            a = article.find('a')
            title = a.text.strip()
            url = a.get('href')

        obj.create_task(
            unique_key=url,
            name=title,
            url=url
        )
