from abc import ABC, abstractmethod
from typing import Dict
from urllib.parse import urlparse

from bs4 import BeautifulSoup, NavigableString

from models.config import ShowDetails
from models.sponsor import Sponsor

class SponsorParseStrategy(ABC):
    @abstractmethod
    def parse(self, page: BeautifulSoup, show_details: ShowDetails) -> Dict[str, Sponsor]:
        pass

class FiresideSponsorParse(SponsorParseStrategy):
    def parse(self, page: BeautifulSoup, show_details: ShowDetails):
        sponsors: Dict[str, Sponsor] = {}

         # Get only the links of all the sponsors
        sponsors_ul = page.find('div',  attrs={'class':'episode-sponsors'}).find('ul')

        if not sponsors_ul:
            return sponsors

        sponsors_links = [a["href"]
                        for a in sponsors_ul.select('li > a:first-child')]

        for sl in sponsors_links:
            try:
                # FIXME: eventually get around to do a more "official" solution
                # Very ugly but works. The goal is to get the hostname of the sponsor
                # link without the subdomain. It would fail on tlds like "co.uk". but I
                # don't think JB had any sponsors like that so it's fine.
                sponsor_slug = ".".join(urlparse(sl).hostname.split(".")[-2:])
                shortname = f"{sponsor_slug}-{show_details.acronym}".lower()

                filename = f"{shortname}.md"

                # Find the <a> element on the page with the link
                sponsor_a = page.find(
                    "div", class_="episode-sponsors").find("a", attrs={"href": sl})
                if sponsor_a and not sponsors.get(filename):
                    sponsors.update({
                        filename: Sponsor(
                            shortname=shortname,
                            title=sponsor_a.find("header").text.strip(),
                            description=sponsor_a.find("p").text.strip(),
                            link=sl
                        )
                    })
            except Exception as e:
                raise

        return sponsors

class PodhomeSponsorParse(SponsorParseStrategy):
    def parse(self, page: BeautifulSoup, show_details: ShowDetails):
        sponsors: Dict[str, Sponsor] = {}

        sponsor_tags = page.find_all('strong', string='Sponsor:') or page.find_all('div', class_='episode-sponsors')

        if not sponsor_tags:
            return sponsors

        for sponsor in sponsor_tags:
            try:
                sponsor_link = sponsor.next_sibling.next_sibling

                # FIXME: eventually get around to do a more "official" solution
                # Very ugly but works. The goal is to get the hostname of the sponsor
                # link without the subdomain. It would fail on tlds like "co.uk". but I
                # don't think JB had any sponsors like that so it's fine.
                sponsor_slug = ".".join(urlparse(sponsor_link['href']).hostname.split(".")[-2:])
                shortname = f"{sponsor_slug}-{show_details.acronym}".lower()

                filename = f'{shortname}.md'

                description = " ".join([sponsor_link.find_next('strong').text, sponsor_link.find_next('strong').next_sibling.text])

                if sponsor_link and not sponsors.get(filename):
                    sponsors.update({
                        filename: Sponsor(
                            shortname=shortname,
                            title=sponsor_link.text.strip(),
                            description=description,
                            link=sponsor_link.get('href')
                        )
                    })
            except Exception as e:
                raise
            except NavigableString:
                pass
        return sponsors

class SponsorParser:
    def __init__(self, page, show_details: ShowDetails, parse_strategy: SponsorParseStrategy):
        self.page = page
        self.parse_strategy = parse_strategy
        self.show_details = show_details

    def run(self):
        return self.parse_strategy.parse(self.page, self.show_details)