import json
from urllib.parse import urljoin
from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)

    for div in soup.find_all('div', {'class': "resource-card button filter-search-cards-card -light-background -large -arrow -link -grid-style"}):
        obj.create_task(
            unique_key=div.find('a').get('href'),
            name=div.find('div', {'class':"cmp-title"}).text.strip(),
            url=urljoin(extras.get('article_base_url'), div.find('a').get('href'))
        )
