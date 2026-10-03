from models.item import Item
from models.podcast import Episode
from scraper import resolve_episode_number

def test_podcast_episode_wins():
    item = Item(title='Anything', link='https://extras.show/94', podcast_episode=Episode(episode='7'))
    assert resolve_episode_number(item) == '7'

def test_itunes_episode_used_when_no_podcast_episode():
    item = Item(title='Anything', link='https://extras.show/94', itunes_episode=7)
    assert resolve_episode_number(item) == '7'

def test_falls_back_to_url():
    # Extras publishes neither tag, so the URL is the only number it gives.
    assert resolve_episode_number(Item(title='Texas LinuxFest Day 2', link='https://extras.show/94')) == '94'

def test_url_wins_over_title():
    # Episode 94 is titled "Clanker Therapy 2: ...", which read as episode 2.
    assert resolve_episode_number(Item(title='Clanker Therapy 2: What We Have Been Building', link='https://extras.show/94')) == '94'

def test_url_ignores_query_string():
    assert resolve_episode_number(Item(title='Road Trip Tech', link='https://extras.show/94/?utm=x')) == '94'

def test_url_with_trailing_slash():
    assert resolve_episode_number(Item(title='Road Trip Tech', link='https://extras.show/94/')) == '94'

def test_falls_back_to_title():
    assert resolve_episode_number(Item(title='78: We Should Know Better', link='https://example.com/latest')) == '78'

def test_no_number_anywhere():
    assert resolve_episode_number(Item(title='No Numbers Here', link='https://example.com/latest')) == ''
