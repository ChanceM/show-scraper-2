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

def test_build_participants_guest_avatar_without_extension(
        mock_settings, mock_configuration, requests_mock, tmp_path):
    """Avatar URLs without a file extension map to a usable filename.

    Extensionless URLs like GitHub /u/<id>?v=4 become
    images/people/<user>.jpg rather than a path built from the URL
    suffix (seen with LUP 689's guest avatar)."""
    mock_settings.DATA_DIR = str(tmp_path)
    PARTICIPANTS.pop('aaron-seigo.md', None)
    img_url = 'https://avatars.githubusercontent.com/u/2236?v=4'
    requests_mock.get(img_url, content=b'\xff\xd8fakejpeg',
                      headers={'content-type': 'image/jpeg'})
    participants = [Person().from_xml(
        f'<podcast:person xmlns:podcast="https://podcastindex.org/namespace/1.0" role="guest" href="https://www.linkedin.com/in/aaronseigo/" img="{img_url}">Aaron Seigo</podcast:person>')]

    try:
        build_participants(participants)
        p = PARTICIPANTS['aaron-seigo.md']
        assert str(p.homepage) == 'https://www.linkedin.com/in/aaronseigo/'
        assert p.avatar == '/images/people/aaron-seigo.jpg'
        assert (tmp_path / 'static' / 'images' / 'people' / 'aaron-seigo.jpg'
                ).read_bytes() == b'\xff\xd8fakejpeg'
    finally:
        PARTICIPANTS.pop('aaron-seigo.md', None)


@pytest.mark.parametrize("url,expected", [
    ('https://example.com/chris.jpg', 'images/people/u.jpg'),
    ('https://example.com/photo.PNG', 'images/people/u.png'),
    ('https://example.com/photo.jpeg', 'images/people/u.jpeg'),
    ('https://example.com/avatar.svg', 'images/people/u.svg'),
    ('https://avatars.githubusercontent.com/u/2236?v=4',
     'images/people/u.jpg'),
    ('https://example.com/avatar', 'images/people/u.jpg'),
    ('https://example.com/avatar.verylongext', 'images/people/u.jpg'),
    ('https://example.com/photo.123', 'images/people/u.jpg'),
    ('https://example.com/photo.jpég', 'images/people/u.jpg'),
])
def test_avatar_relpath(url, expected):
    from scraper import avatar_relpath
    assert avatar_relpath(url, 'u') == expected