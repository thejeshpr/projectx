import json
import logging
import time
import urllib.parse

from crawler_backend import WebClient, BaseParser

from newspaper import Article

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    key = obj.get_config_val('nwsapi_key')
    base_url = base_url.format(key=key)
    res = WebClient.get(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    if res.status_code == 200:
        json_data = res.json()

        if json_data['status'] == 'ok':
            for article in json_data.get('articles'):
                name = f"{article.get('author', '?')} - {article.get('title')}"
                url = article["url"]

                created_obj = obj.create_task(
                    unique_key=article["url"],
                    name=name,
                    url=url,
                    # data=article_extractor(url)
                )

                # article extraction is not needed at this moment
                # if created_obj:
                #     time.sleep(1)


def article_extractor(url):
    try:
        article = Article(url, language="en")
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Article extraction error: {e}")
        return f"Article Extraction ERROR: {e}"

