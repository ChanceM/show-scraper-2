from models.podcast import Guid
from uuid import UUID

def test_podcast_guid():
    assert Guid(root='daddde30-f61d-47d2-9f59-a8fcc4d2e68d').root == UUID('daddde30-f61d-47d2-9f59-a8fcc4d2e68d')
    assert Guid(root='11ccb502-6a54-46a5-8e40-5226b495de04').root == UUID('11ccb502-6a54-46a5-8e40-5226b495de04')
    assert Guid(root='11ccb502-6a54-46a5-8e40-5226b495de04').to_xml() == b'<podcast:guid xmlns:podcast="https://podcastindex.org/namespace/1.0">11ccb502-6a54-46a5-8e40-5226b495de04</podcast:guid>'