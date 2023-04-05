import json
import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)
    extras = json.loads(obj.site_conf.extra_data_json)
    post_base_url = extras.get("post_base_url", "")

    # find banner posts
    for div in soup.find_all('div', {'class':'flex-1'}):
        a = div.find('a', {'class': 'block w-full text-lg font-semibold leading-tight mt-2'})

        if a:
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=a.text.strip(),
                url=a.attrs.get('href')
            )

    # find remaining posts
    for a in soup.find_all('a', {'class':'block text-primary-400 font-semibold leading-6 text-lg header-500 md:text-xl'}):
        obj.create_task(
            unique_key=urllib.parse.urljoin(post_base_url,a.attrs.get('href')),
            name=a.text.strip(),
            url=urllib.parse.urljoin(post_base_url,a.attrs.get('href'))
        )



