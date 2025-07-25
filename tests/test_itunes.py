from models.itunes import Category, Duration, Explicit, Keywords
from datetime import time

def test_itunes_explicit():
    assert Explicit(root='yes').root == 'yes'
    assert Explicit(root='no').root == 'no'
    assert Explicit(root=True).root == 'yes'
    assert Explicit(root=False).root == 'no'
    assert Explicit(root=1).root == 'yes'
    assert Explicit(root=0).root == 'no'
    assert Explicit(root=0).to_xml() == b'<itunes:explicit xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">no</itunes:explicit>'
    assert Explicit(root=0) == Explicit.from_xml(b'<itunes:explicit xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">no</itunes:explicit>')


def test_itunes_duration():
    assert Duration(root='00:00:01').root == time.fromisoformat('00:00:01')
    assert Duration(root='00:34:01').root == time.fromisoformat('00:34:01')
    assert Duration(root='1:34:01').root == time.fromisoformat('01:34:01')
    assert Duration(root='1:4:01').root == time.fromisoformat('01:04:01')
    assert Duration(root='1:4:1').root == time.fromisoformat('01:04:01')
    assert Duration(root=10).root == time.fromisoformat('00:00:10')
    assert Duration(root=90).root == time.fromisoformat('00:01:30')
    assert Duration(root=4205).root == time.fromisoformat('01:10:05')
    assert Duration(root=4205).to_xml() == b'<itunes:duration xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">01:10:05</itunes:duration>'
    assert Duration(root=4205) == Duration.from_xml(b'<itunes:duration xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">01:10:05</itunes:duration>')

def test_itunes_keywords():
    assert Keywords(keywords='tag1,tag2,tag3').keywords == ['tag1','tag2','tag3']
    assert Keywords(keywords='tag1,tag2,tag3').keywords[0] == 'tag1'
    assert Keywords(keywords='tag1,tag2,tag3').keywords[1] == 'tag2'
    assert Keywords(keywords='tag1,tag2,tag3').keywords[2] == 'tag3'
    assert Keywords.from_xml(b'<itunes:keywords xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">tag1,tag2,tag3</itunes:keywords>') == Keywords(keywords='tag1,tag2,tag3')
    assert Keywords(keywords='tag1,tag2,tag3').to_xml() == b'<itunes:keywords xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd">tag1,tag2,tag3</itunes:keywords>'

def test_itunes_category():
    assert Category.from_xml('<itunes:category xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" text="News"><itunes:category text="Tech News"/></itunes:category>') == Category(text='News', category=Category(text='Tech News'))
    assert Category.from_xml('<itunes:category xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" text="News"><itunes:category text="Tech News"/></itunes:category>').category.text == 'Tech News'
    assert Category.from_xml('<itunes:category xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" text="News"><itunes:category text="Tech News"/></itunes:category>').text == 'News'
    assert Category.from_xml('<itunes:category xmlns:itunes="http://www.itunes.com/dtds/podcast-1.0.dtd" text="News"/>') == Category(text='News')
