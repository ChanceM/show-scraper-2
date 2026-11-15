import yaml
from pytest import mark

from models.config import ConfigData
from models.participant import Participant
from scraper import process_and_serialize_object

MERGED_PEOPLE = [
    'carl-george.md', 'jeremy-soller.md', 'kent-overstreet.md', 'matthew-miller.md',
    'paulus-schoutsen.md', 'dustymabe.md', 'jon-seager.md', 'michaeltunnell.md',
]


@mark.parametrize('filename', MERGED_PEOPLE)
def test_merged_people_are_not_overridden(mocker, tmp_path, filename):
    with open('config.yml') as file:
        config = ConfigData(**yaml.load(file, Loader=yaml.SafeLoader))
    mocker.patch('scraper.CONFIGURATION', config)
    original = '---\ntype: guest\nusername: x\ntitle: X\nbio: hand merged\n---\n'
    (tmp_path / filename).write_text(original)

    process_and_serialize_object(filename, Participant(type='guest', username='x', title='X',
                                                       avatar='/images/people/new.png'), tmp_path, overwrite=True)

    assert (tmp_path / filename).read_text() == original
