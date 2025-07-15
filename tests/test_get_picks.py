from types import SimpleNamespace
from pydantic import AnyHttpUrl
import pytest
from models.config import ShowDetails
from models.pick import Pick, PickShow
from scraper import get_picks
from unittest.mock import patch, mock_open

@pytest.fixture
def mock_settings(mocker):
    return mocker.patch('scraper.Settings', SimpleNamespace(DATA_DIR = 'data'))


@pytest.mark.parametrize("test_input,expected",
  [
      ('''<li><a title="Pick: bitchat" href="https://bitchat.free/" rel="nofollow">Pick: bitchat</a></li>''', [Pick(title='bitchat', url=AnyHttpUrl('https://bitchat.free/'), description=None, shows=[PickShow(show='This Week In Bitcoin', episode=1, slug='test')], license=None)])
      , ('''<li><a title="Pick: bitchat" href="https://bitchat.free/" ref="nofollow">Pick: bitchat</a>FIXED</li>''', [Pick(title='bitchat', url=AnyHttpUrl('https://bitchat.free/'), description='FIXED', shows=[PickShow(show='This Week In Bitcoin', episode=1, slug='test')], license=None)])
  ]
)

def test_get_picks(test_input, expected, mock_settings):
    with patch('builtins.open', mock_open()) as mocked_file:
        assert get_picks(test_input,1,'test',ShowDetails(
            show_rss='https://serve.podhome.fm/rss/55b53584-4219-4fb0-b916-075ce23f714e',
            show_url='https://www.thisweekinbitcoin.show/',
            jb_url='https://www.jupiterbroadcasting.com/show/this-week-in-bitcoin',
            acronym='twib',
            name='This Week In Bitcoin',
            host_platform='podhome')) == expected