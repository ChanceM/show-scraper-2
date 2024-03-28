from models.podcast import Person
from scraper import get_canonical_username


def test_known_usernames(mocker):
    mocker.patch('scraper.config', {
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
    })

    assert get_canonical_username(Person(name='Chris Fisher')) == 'chris'
    assert get_canonical_username(Person(name='chrislas')) == 'chris'
    assert get_canonical_username(Person(name='drewdevore')) == 'drew-devore'
    assert get_canonical_username(Person(name='drewdvore')) == 'drew-devore'
    assert get_canonical_username(Person(name='drewofdoom')) == 'drew-devore'

def test_unknown_usernames(mocker):
    mocker.patch('scraper.config', {
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
    })

    assert get_canonical_username(Person(name='user')) == 'user'
    assert get_canonical_username(Person(name='user-01')) == 'user-01'
    assert get_canonical_username(Person(name='l33t~h@xor')) == 'l33t~h@xor'