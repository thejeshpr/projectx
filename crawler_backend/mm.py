import logging

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    logging.info("Establishing connection to url")
    base_url = obj.site_conf.base_url
    soup = WebClient.get_soup_phjs(base_url)

    tasks = []

    divs = soup.find_all('div', {'class':'entry-grid-content hgrid-span-12'})

    for div in divs[::-1]:
        h2 = div.find("h2", {"class": "entry-title"})
        a = h2.find('a')

        url = a.get('href')
        name = a.text.strip()

        desc_div = div.find("div", {"class": "entry-summary"})
        if desc_div:
            desc = desc_div.text.strip()

        tasks.append(
            dict(
                name=name,
                url=url,
                unique_key=url,
                data=desc
            )
        )

    logging.debug(f"found {len(tasks)}")
    return tasks
