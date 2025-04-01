import pytest
from types import SimpleNamespace

from scraper import PARTICIPANTS, build_participants
from models.config import ConfigData
from models.podcast import Person
from models.participant import Participant

@pytest.fixture
def mock_settings(mocker):
    return mocker.patch('scraper.Settings', SimpleNamespace(Host_Roles=['Host', 'Co-Host'], Guest_Roles=['Guest']))

@pytest.fixture
def mock_configuration(mocker):
    return mocker.patch('scraper.CONFIGURATION', ConfigData(**{'shows': {}, 'data_dont_override': set(),
        'usernames_map': {
            'chris': {
                'Chris Fisher'
                ,'chrislas'
            }
            , 'wes': {
                'Wes Payne'
                ,'wespayne'
            }
            , 'drew-devore': {
                'drewdevore'
                ,'drewdvore'
                ,'drewofdoom'
            }
        }
    }))

def test_build_participants(mock_settings, mock_configuration):
    participants = [
        Person().from_xml('<podcast:person xmlns:podcast="https://podcastindex.org/namespace/1.0" group="cast" role="host"  href="https://chrislas.com">Chris Fisher</podcast:person>'),
        Person().from_xml('<podcast:person xmlns:podcast="https://podcastindex.org/namespace/1.0" group="cast" role="host" href="https://www.jupiterbroadcasting.com/hosts/wes">Wes Payne</podcast:person>')
    ]

    expected_participants = {
        'chris.md': Participant(type='host', username='chris', title='Chris Fisher', bio=None, avatar=None, avatar_small=None, homepage="https://chrislas.com", twitter=None, linkedin=None, instagram=None, youtube=None),
        'wes.md': Participant(type='host', username='wes', title='Wes Payne', bio=None, avatar=None, avatar_small=None, homepage="https://www.jupiterbroadcasting.com/hosts/wes", twitter=None, linkedin=None, instagram=None, youtube=None),
    }

    build_participants(participants)
    assert PARTICIPANTS == expected_participants