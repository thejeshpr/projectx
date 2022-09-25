import logging

from crawler_backend import BaseParser, WebClient

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    logging.info("Establishing connection to url")
    res = WebClient.get(obj.site_conf.base_url)

    logging.debug(f"status code:{res.status_code}")
    data = res.json()
    logging.debug(f"json data: {data}")

    tasks = []

    for repo in data:
        logging.debug(repo)
        tasks.append(
            dict(
                name=repo.get("repositoryName"),
                url=repo.get("url"),
                unique_key=repo.get("repositoryName"),
                data=repo.get("url")
            )
        )
    logging.debug(f"found {len(tasks)}")
    return tasks
