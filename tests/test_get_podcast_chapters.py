from types import SimpleNamespace
import pytest
from models import episode
from models.episode import Chapter
from models.podcast import Chapters
from scraper import get_podcast_chapters

@pytest.fixture
def mock_settings(mocker):
    return mocker.patch('scraper.Settings', SimpleNamespace(Retry_Count = 3))

def test_get_podcast_chapters(mock_settings):
    assert get_podcast_chapters(Chapters(url='https://assets.podhome.fm/f01a19c0-6f9d-4aef-9515-08dc15242149/63859878681582155886fad73e-7543-44c0-88c5-3db439e16679v1.chapters.json',type='appliction/json')) == episode.Chapters(version='1.2.0', chapters=[Chapter(startTime=0, title='Welcome into 23', img=None, url=None, toc=None, endTime=None, location=None), Chapter(startTime=43, title='Bitcoin Headlines and Market Insights', img=None, url=None, toc=None, endTime=None, location=None), Chapter(startTime=181, title='Job Market Shifts and Economic Signals', img=None, url=None, toc=None, endTime=None, location=None), Chapter(startTime=733, title='Thoughts on Life and Key Man Risk', img=None, url=None, toc=None, endTime=None, location=None), Chapter(startTime=934, title='Supporting the Show: Affiliates and Boosts', img=None, url=None, toc=None, endTime=None, location=None), Chapter(startTime=989, title='Listener Boosts and Feedback', img=None, url=None, toc=None, endTime=None, location=None), Chapter(startTime=1819, title='Understanding KYC and Wallets', img=None, url=None, toc=None, endTime=None, location=None), Chapter(startTime=2181, title='Newbies Corner: KYC Explained', img=None, url=None, toc=None, endTime=None, location=None), Chapter(startTime=2734, title='Project Updates and Exciting Innovations', img=None, url=None, toc=None, endTime=None, location=None), Chapter(startTime=3019, title='Debasement Analogy: Taylor Swift Tickets', img=None, url=None, toc=None, endTime=None, location=None), Chapter(startTime=3246, title='Swamp Thing', img=None, url=None, toc=None, endTime=None, location=None)], author=None, title='Employment Shock Drop', podcastName='This Week in Bitcoin', description=None, fileName=None, waypoints=None)
    assert get_podcast_chapters(Chapters(url='https://assets.podhome.fm/f01a19c0-6f9d-4aef-9515-08dc15242149/63859878681582155886fad73e-7543-44c0-88c5-3db439e16679v2.chapters.json',type='appliction/json')) == None