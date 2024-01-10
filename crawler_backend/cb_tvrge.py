import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    # extras = json.loads(obj.site_conf.extra_data_json)

    items_found = dict()
    for item in soup.find_all('h2', {'class': 'font-polysans text-20 font-bold leading-100 tracking-1 md:text-24 lg:text-20'}):
        a = item.find('a')
        if a and a.get('href'):
            items_found[a.get('href')] = a.text.strip()

    for item in soup.find_all('a', {'class':'text-white hover:text-franklin'}):
        if item and item.get('href'):
            items_found[item.get('href')] = item.text.strip()

    for item in soup.find_all('h2', {'class': 'font-polysans text-20 font-bold leading-100 tracking-1 md:text-24'}):
        a = item.find('a')
        if a and a.get('href'):
            items_found[a.get('href')] = a.text.strip()

    for item in soup.find_all('div', {'class':'duet--content-cards--content-card relative flex flex-row border-b border-solid border-gray-cc px-0 last-of-type:border-b-0 dark:border-gray-31 py-16 hover:bg-[#FBF9FF] dark:hover:bg-gray-18 max-w-container-sm last-of-type:border-b-0 md:px-10 lg:py-24'}):
        a = item.find('a')
        div = item.find('div', {'class': 'inline pr-4 text-17 font-bold md:text-17'})
        if a and a.get('href') and div:
            items_found[a.get('href')] = div.text.strip()

    for key, val in items_found.items():
        url = urllib.parse.urljoin(base_url, key)
        obj.create_task(
            unique_key=url,
            name=val,
            url=url,
        )

