import json
import urllib

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    res = WebClient.post_phjs(base_url, return_json=True)
    extras = json.loads(obj.site_conf.extra_data_json)

    posts = res['result']['data']['nodes'][::-1]

    for post in posts:
        post['text'] = urllib.parse.urljoin(extras['article_base_url'], post.get('articleLink'))
        obj.create_task(
            unique_key=post.get('id'),
            name=post['title'],
            url=post['text']
        )