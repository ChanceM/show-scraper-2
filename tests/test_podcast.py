from models.podcast import Guid, Episode
from uuid import UUID

def test_podcast_guid():
    assert Guid(root='daddde30-f61d-47d2-9f59-a8fcc4d2e68d').root == UUID('daddde30-f61d-47d2-9f59-a8fcc4d2e68d')
    assert Guid(root='11ccb502-6a54-46a5-8e40-5226b495de04').root == UUID('11ccb502-6a54-46a5-8e40-5226b495de04')
    assert Guid(root='11ccb502-6a54-46a5-8e40-5226b495de04').to_xml() == b'<podcast:guid xmlns:podcast="https://podcastindex.org/namespace/1.0">11ccb502-6a54-46a5-8e40-5226b495de04</podcast:guid>'
    assert Guid.from_xml(b'<podcast:guid xmlns:podcast="https://podcastindex.org/namespace/1.0">11ccb502-6a54-46a5-8e40-5226b495de04</podcast:guid>') == Guid(root='11ccb502-6a54-46a5-8e40-5226b495de04')

def test_podcast_episode():
    assert Episode(display='ep1', episode='1').episode == '1'
    assert Episode(display='ep1', episode='1').display == 'ep1'
    assert Episode(display='ep1', episode='1').to_xml() == b'<podcast:episode xmlns:podcast="https://podcastindex.org/namespace/1.0" display="ep1">1</podcast:episode>'
    assert Episode.from_xml(b'<podcast:episode xmlns:podcast="https://podcastindex.org/namespace/1.0" display="ep1">1</podcast:episode>') == Episode(display='ep1', episode='1')