import json
import logging
import urllib.parse
import praw

from crawler_backend import WebClient, BaseParser


def scrape(obj: BaseParser):
    logging.info("Establishing connection using praw")
    extras = json.loads(obj.site_conf.extra_data_json)

    rdt = praw.Reddit(
        client_id=BaseParser.get_config_val("rdt_cl_id"),
        client_secret=BaseParser.get_config_val("rdt_cl_srt"),
        user_agent=BaseParser.get_config_val("rdt_usr_agt")
    )

    for i, sub in enumerate(rdt.subreddit(extras.get("sr")).new(), 1):
        logging.debug(f"{i} processing rdt {sub.title}")
        obj.create_task(
            unique_key=sub.id,
            name=sub.title,
            url=sub.url,
            data=f"created_at: {sub.created}\n"
                 f"text: {sub.selftext}"
        )

