from scraper import parse_episode_number

def test_parse_episode_number():
    assert parse_episode_number('EPISODE 1: THIS IS A TEST') == '1'
    assert parse_episode_number('EPISODE 122: THIS IS A TEST 123') == '122'
    assert parse_episode_number('555: Glide like a Goose, Honk like a Moose') == '555'
    assert parse_episode_number('Pocket Office 3: We\'ll do it LIVE!') == 'Pocket Office 3'