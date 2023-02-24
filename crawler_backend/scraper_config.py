from .cb_gh_trending import scrape as GH_Trending_Scraper
from .cb_bkdko import scrape as BKDKO_Scraper
from .cb_crdko import scrape as CRDKO_Scraper
from .cb_mm import scrape as MM_Scraper
from .cb_d2 import scrape as D2_Scraper
from .cb_rdt import scrape as RDT_Scraper
from .cb_spny import scrape as SNPY_Scraper
from .cb_ng import scrape as NG_Scraper
from .cb_rp import scrape as RP_Scraper
from .cb_dzne import scrape as DZNE_Scraper
from .cb_bpanda import scrape as BPANDA_Scraper
from .cb_twrds import scrape as TWRDS_Scraper


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
