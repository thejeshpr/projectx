import logging
import urllib.parse

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    base_url = obj.site_conf.base_url
    soup = WebClient.get_bs(base_url)

    # find banner posts
    for div in soup.find_all('div', {'class': "c-entry-box-base c-entry-box-hero"}):
        # find links
        a = div.find('a')
        if a:
            url = a.attrs.get('href')
            h3 = div.find('h3', {'class': 'c-entry-box-base__headline'})

            # find titles
            if h3:
                a = h3.find('a')
                url = url
                obj.create_task(
                    unique_key=url,
                    name=a.text.strip(),
                    url=url
                )

    # find remaining posts
    for h2 in soup.find_all('h2', {'class': 'c-entry-box--compact__title'}):
        a = h2.find('a')
        if a:
            obj.create_task(
                unique_key=a.attrs.get('href'),
                name=a.text.strip(),
                url=a.attrs.get('href')
            )
