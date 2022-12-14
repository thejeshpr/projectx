from .gh_trending import scrape as GH_Trending_Scraper
from .bkdko import scrape as BKDKO_Scraper
from .crdko import scrape as CRDKO_Scraper
from .mm import scrape as MM_Scraper
from .d2 import scrape as D2_Scraper
from .rdt import scrape as RDT_Scraper
from .spny import scrape as SNPY_Scraper
from .ng import scrape as NG_Scraper
from .rp import scrape as RP_Scraper
from .dzne import scrape as DZNE_Scraper
from .bpanda import scrape as BPANDA_Scraper
from .twrds import scrape as TWRDS_Scraper


def get_scrapper(name):
    scrapers = dict(
        gh_trending=GH_Trending_Scraper,
        bkdko=BKDKO_Scraper,
        crdko=CRDKO_Scraper,
        mm=MM_Scraper,
        d2=D2_Scraper,
        rdt=RDT_Scraper,
        spny=SNPY_Scraper,
        ng=NG_Scraper,
        rp=RP_Scraper,
        dzne=DZNE_Scraper,
        bpanda=BPANDA_Scraper,
        twrds=TWRDS_Scraper,
    )
    if name in scrapers.keys():
        return scrapers.get(name)
    else:
        raise f"invalid scrapper name: {name}"
