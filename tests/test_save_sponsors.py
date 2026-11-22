from frontmatter import loads
from bs4 import BeautifulSoup
from types import SimpleNamespace

from models.config import ShowDetails
from models.sponsor import Sponsor
from models.strategies.sponsor import FiresideSponsorParse
from scraper import process_and_serialize_object, save_sponsors
import scraper

SPONSOR = Sponsor(shortname='linode.com-lup', title='Linode', description='Cloud hosting: $100 credit.',
                  link='https://linode.com/unplugged', episode=500)


def test_sponsor_written_as_data_yaml(mocker, tmp_path):
    mocker.patch('scraper.CONFIGURATION', SimpleNamespace(data_dont_override=set()))
    process_and_serialize_object('linode.com-lup.yaml', SPONSOR, tmp_path)

    text = (tmp_path / 'linode.com-lup.yaml').read_text()
    assert text.startswith('---\n') and text.endswith('\n---'), 'same --- delimited format as data/picks'
    assert loads(text).metadata == {'title': 'Linode', 'description': 'Cloud hosting: $100 credit.',
                                    'link': 'https://linode.com/unplugged', 'episode': 500}


def test_sponsor_without_episode_omits_it(mocker, tmp_path):
    mocker.patch('scraper.CONFIGURATION', SimpleNamespace(data_dont_override=set()))
    process_and_serialize_object('x.yaml', SPONSOR.model_copy(update={'episode': None}), tmp_path)

    assert 'episode' not in loads((tmp_path / 'x.yaml').read_text()).metadata


def test_newer_sponsor_replaces_older(mocker, tmp_path):
    mocker.patch('scraper.CONFIGURATION', SimpleNamespace(data_dont_override=set()))
    process_and_serialize_object('linode.com-lup.yaml', SPONSOR, tmp_path)
    newer = SPONSOR.model_copy(update={'description': 'New read.', 'episode': 501})
    process_and_serialize_object('linode.com-lup.yaml', newer, tmp_path, overwrite=True)

    assert loads((tmp_path / 'linode.com-lup.yaml').read_text()).metadata['description'] == 'New read.'


def test_older_sponsor_keeps_newer_file(mocker, tmp_path):
    mocker.patch('scraper.CONFIGURATION', SimpleNamespace(data_dont_override=set()))
    process_and_serialize_object('linode.com-lup.yaml', SPONSOR, tmp_path)
    older = SPONSOR.model_copy(update={'description': 'Old read.', 'episode': 499})
    process_and_serialize_object('linode.com-lup.yaml', older, tmp_path, overwrite=True)

    assert loads((tmp_path / 'linode.com-lup.yaml').read_text()).metadata['description'] == SPONSOR.description


def test_save_sponsors_writes_to_data_dir(mocker, tmp_path):
    mocker.patch('scraper.CONFIGURATION', SimpleNamespace(data_dont_override=set()))
    mocker.patch('scraper.Settings', SimpleNamespace(DATA_DIR=str(tmp_path), Overwrite_Existing=True))
    mocker.patch.dict(scraper.SPONSORS, {'linode.com-lup.yaml': SPONSOR}, clear=True)
    with scraper.concurrent.futures.ThreadPoolExecutor() as executor:
        save_sponsors(executor)

    assert (tmp_path / 'data' / 'sponsors' / 'linode.com-lup.yaml').exists()
    assert not (tmp_path / 'content' / 'sponsors').exists()


def test_parsed_sponsor_keyed_by_yaml_filename():
    page = BeautifulSoup('<div class="episode-sponsors"><ul><li><a href="https://linode.com/unplugged">'
                         '<header>Linode</header><p>Cloud hosting.</p></a></li></ul></div>', 'html.parser')
    sponsors = FiresideSponsorParse().parse(page, ShowDetails(
        show_rss='https://feeds.jupiterbroadcasting.com/lup',
        show_url='https://linuxunplugged.com',
        jb_url='https://www.jupiterbroadcasting.com/show/linux-unplugged',
        acronym='lup',
        name='LINUX Unplugged',
        host_platform='fireside'), 500)

    assert list(sponsors) == ['linode.com-lup.yaml']
