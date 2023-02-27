import logging

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    logging.info("Establishing connection to url")
    base_url = obj.site_conf.base_url
    soup = WebClient.get_soup_phjs(base_url)

    divs = soup.find_all('div', {'class': 'entry-grid-content hgrid-span-12'})

    for div in divs[::-1]:
        h2 = div.find("h2", {"class": "entry-title"})
        a = h2.find('a')

        url = a.get('href')
        name = a.text.strip()

        desc_div = div.find("div", {"class": "entry-summary"})

        desc = desc_div.text.strip() if desc_div else None

        obj.create_task(
            unique_key=url,
            name=name,
            url=url,
            data=desc
        )
