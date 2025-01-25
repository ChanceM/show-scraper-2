import pytest
from models.config import ConfigData
from models.podcast import Person
from scraper import get_canonical_username

@pytest.fixture
def mock_configuration(mocker):
    return mocker.patch('scraper.CONFIGURATION', ConfigData(**{'shows': {}, 'data_dont_override': set(),
        'usernames_map': {
            'chris': {
                'Chris Fisher'
                ,'chrislas'
            }
            , 'drew-devore': {
                'drewdevore'
                ,'drewdvore'
                ,'drewofdoom'
            }
        }
    }))

def test_known_usernames(mock_configuration):
    assert get_canonical_username(Person(name='Chris Fisher')) == 'chris'
    assert get_canonical_username(Person(name='chrislas')) == 'chris'
    assert get_canonical_username(Person(name='drewdevore')) == 'drew-devore'
    assert get_canonical_username(Person(name='drewdvore')) == 'drew-devore'
    assert get_canonical_username(Person(name='drewofdoom')) == 'drew-devore'

def test_unknown_usernames(mock_configuration):
    assert get_canonical_username(Person(name='user')) == 'user'
    assert get_canonical_username(Person(name='user-01')) == 'user-01'
    assert get_canonical_username(Person(name='l33t~h@xor')) == 'l33t~h@xor'
    assert get_canonical_username(Person(name='Producer Jeff')) == 'producer-jeff'