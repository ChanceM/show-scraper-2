from bs4 import BeautifulSoup
from models.strategies.sponsor import FiresideSponsorParse
from scraper import parse_sponsors
from models.config import ShowDetails

def test_parse_sponsors_multiple(requests_mock):
    requests_mock.get('http://example.com', text='<strong>Sponsor:</strong> <a href="http://podhome.fm" target="_blank">http://podhome.fm</a><br /> <strong>Promo Code:</strong> TWIB<br /><br /><strong>River Affiliate Link Sponsor:</strong> <a href="https://river.com/signup?r=3CT4V56E" target="_blank">Buy Sats on River</a><br /><br />')
    assert parse_sponsors('http://example.com', '1', 'twib', ShowDetails(
        show_rss='https://serve.podhome.fm/rss/55b53584-4219-4fb0-b916-075ce23f714e',
        show_url='https://www.thisweekinbitcoin.show/',
        jb_url='https://www.jupiterbroadcasting.com/show/this-week-in-bitcoin',
        acronym='twib',
        name='This Week In Bitcoin',
        host_platform='podhome')) == ['podhome.fm-twib','river.com-twib']

def test_parse_sponsors_single(requests_mock):
    requests_mock.get('http://example.com', text='<strong>Sponsor:</strong> <a href="http://podhome.fm" target="_blank">http://podhome.fm</a><br /> <strong>Promo Code:</strong> TWIB<br /><br />')
    assert parse_sponsors('http://example.com', '1', 'twib', ShowDetails(
        show_rss='https://serve.podhome.fm/rss/55b53584-4219-4fb0-b916-075ce23f714e',
        show_url='https://www.thisweekinbitcoin.show/',
        jb_url='https://www.jupiterbroadcasting.com/show/this-week-in-bitcoin',
        acronym='twib',
        name='This Week In Bitcoin',
        host_platform='podhome')) == ['podhome.fm-twib']

def test_live_sponsor():
    assert parse_sponsors('https://linuxunplugged.com/664', '664', 'lup', ShowDetails(
        show_rss='https://feeds.jupiterbroadcasting.com/lup',
        show_url='https:/linux-unplugged.show',
        jb_url='https://www.jupiterbroadcasting.com/show/linux-unplugged',
        acronym='lup',
        name='LINUX Unplugged',
        host_platform='fireside')) == ['defined.net-lup','memberful.com-lup']

def test_fireside_no_sponsors():
    # Most Extras episodes have no sponsor block, so parse() used to raise.
    # parse_sponsors catches that and logs a warning, so enabling Extras
    # meant a warning per episode and no sponsor data written.
    page = BeautifulSoup('<div class="episode"></div>', 'html.parser')
    assert FiresideSponsorParse().parse(page, ShowDetails(
        show_rss='https://extras.show/rss',
        show_url='https://extras.show',
        jb_url='https://www.jupiterbroadcasting.com/show/jupiter-extras',
        acronym='JE',
        name='Jupiter EXTRAS',
        host_platform='fireside'), 92) == {}
