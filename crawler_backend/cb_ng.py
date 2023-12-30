import json
import logging

from crawler_backend import WebClient, BaseParser

logging.getLogger(__name__)


def scrape(obj: BaseParser):
    arg = json.loads(obj.site_conf.extra_data_json)
    grp, typ = arg.get("grp"), arg.get("typ")
    base_url = obj.site_conf.base_url
    base_url = base_url.format(grp=grp, typ=typ)
    data = WebClient.post_phjs(base_url, return_json=True)

    posts = data.get("data").get("posts")[::-1]
    logging.debug(posts)

    for post in posts:

        data = {
            "caption": "{}\n{}".format(post.get("title"), post.get("url")),
            "title": post.get("title"),
            "nsfw": post.get("nsfw"),
            "post_url": post.get("url"),
            "content_type": post.get("type"),
            "up_vote": post.get("upVoteCount"),
            "down_vote": post.get("downVoteCount"),
            "description": post.get("description"),
            "comments_count": post.get("commentsCount"),
        }

        # check post type
        if post["type"] == "Photo":
            data["url"] = post.get("images").get("image700").get("url")
            obj.create_task(
                unique_key=post.get("id"),
                name=post['title'],
                url=data["url"],
                data=f'URL: {post.get("url")}'
            )

        elif post["type"] == "Animated":
            data["url"] = post.get("images").get("image460sv").get("url")
            obj.create_task(
                unique_key=post.get("id"),
                name=post['title'],
                url=data["url"],
                data=f'URL: {post.get("url")}'
            )

