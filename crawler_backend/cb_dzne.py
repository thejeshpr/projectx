import json
import urllib

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)

    a_list = soup.find_all('a', {'class': 'article-title link-hover-underline-blue'})

    for a in a_list:
        article_url = urllib.parse.urljoin(extras['article_base_url'], a.get('href'))
        obj.create_task(
            unique_key=article_url,
            name=a.text.strip(),
            url=article_url
        )
