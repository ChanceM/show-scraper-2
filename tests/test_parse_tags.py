from scraper import parse_tags
from models.config import ShowDetails

def test_parse_tags_fireside(requests_mock):
    requests_mock.get('http://example.com', text='<h5>Tags</h5> <div class="tags"> <a class="tag" href="/tags/btrfs%20assistant"><i class="fas fa-tag" aria-hidden="true"></i> btrfs assistant</a> <a class="tag" href="/tags/sched-ext"><i class="fas fa-tag" aria-hidden="true"></i> sched-ext</a> <a class="tag" href="/tags/rusticl"><i class="fas fa-tag" aria-hidden="true"></i> rusticl</a> <a class="tag" href="/tags/zram"><i class="fas fa-tag" aria-hidden="true"></i> zram</a> <a class="tag" href="/tags/burstiness"><i class="fas fa-tag" aria-hidden="true"></i> burstiness</a> <a class="tag" href="/tags/rt%20kernel"><i class="fas fa-tag" aria-hidden="true"></i> rt kernel</a> <a class="tag" href="/tags/bore"><i class="fas fa-tag" aria-hidden="true"></i> bore</a> <a class="tag" href="/tags/scheduler"><i class="fas fa-tag" aria-hidden="true"></i> scheduler</a> <a class="tag" href="/tags/arch"><i class="fas fa-tag" aria-hidden="true"></i> arch</a> <a class="tag" href="/tags/chatgippity"><i class="fas fa-tag" aria-hidden="true"></i> chatgippity</a> <a class="tag" href="/tags/flatpak"><i class="fas fa-tag" aria-hidden="true"></i> flatpak</a> <a class="tag" href="/tags/kernel%20developers"><i class="fas fa-tag" aria-hidden="true"></i> kernel developers</a> <a class="tag" href="/tags/linux%20kernel"><i class="fas fa-tag" aria-hidden="true"></i> linux kernel</a> <a class="tag" href="/tags/regressions"><i class="fas fa-tag" aria-hidden="true"></i> regressions</a> <a class="tag" href="/tags/cachyos"><i class="fas fa-tag" aria-hidden="true"></i> cachyos</a> <a class="tag" href="/tags/linux%20unplugged"><i class="fas fa-tag" aria-hidden="true"></i> linux unplugged</a> <a class="tag" href="/tags/linux%20podcast"><i class="fas fa-tag" aria-hidden="true"></i> linux podcast</a> <a class="tag" href="/tags/jupiter%20broadcasting"><i class="fas fa-tag" aria-hidden="true"></i> jupiter broadcasting</a> </div>')
    assert parse_tags('http://example.com','1','lup', ShowDetails(
        show_rss='https://serve.podhome.fm/rss/55b53584-4219-4fb0-b916-075ce23f714e',
        show_url='https://www.thisweekinbitcoin.show/',
        jb_url='https://www.jupiterbroadcasting.com/show/this-week-in-bitcoin',
        acronym='twib',
        name='This Week In Bitcoin',
        host_platform='fireside')) == [
            "arch",
            "bore",
            "btrfs assistant",
            "burstiness",
            "cachyos",
            "chatgippity",
            "flatpak",
            "jupiter broadcasting",
            "kernel developers",
            "linux kernel",
            "linux podcast",
            "linux unplugged",
            "regressions",
            "rt kernel",
            "rusticl",
            "sched-ext",
            "scheduler",
            "zram"
        ]

def test_parse_tags_podhome(requests_mock):
    requests_mock.get('http://example.com', text='<h5>Tags</h5> <div class="tags"> <a class="tag" href="/tags/btrfs%20assistant"><i class="fas fa-tag" aria-hidden="true"></i> btrfs assistant</a> <a class="tag" href="/tags/sched-ext"><i class="fas fa-tag" aria-hidden="true"></i> sched-ext</a> <a class="tag" href="/tags/rusticl"><i class="fas fa-tag" aria-hidden="true"></i> rusticl</a> <a class="tag" href="/tags/zram"><i class="fas fa-tag" aria-hidden="true"></i> zram</a> <a class="tag" href="/tags/burstiness"><i class="fas fa-tag" aria-hidden="true"></i> burstiness</a> <a class="tag" href="/tags/rt%20kernel"><i class="fas fa-tag" aria-hidden="true"></i> rt kernel</a> <a class="tag" href="/tags/bore"><i class="fas fa-tag" aria-hidden="true"></i> bore</a> <a class="tag" href="/tags/scheduler"><i class="fas fa-tag" aria-hidden="true"></i> scheduler</a> <a class="tag" href="/tags/arch"><i class="fas fa-tag" aria-hidden="true"></i> arch</a> <a class="tag" href="/tags/chatgippity"><i class="fas fa-tag" aria-hidden="true"></i> chatgippity</a> <a class="tag" href="/tags/flatpak"><i class="fas fa-tag" aria-hidden="true"></i> flatpak</a> <a class="tag" href="/tags/kernel%20developers"><i class="fas fa-tag" aria-hidden="true"></i> kernel developers</a> <a class="tag" href="/tags/linux%20kernel"><i class="fas fa-tag" aria-hidden="true"></i> linux kernel</a> <a class="tag" href="/tags/regressions"><i class="fas fa-tag" aria-hidden="true"></i> regressions</a> <a class="tag" href="/tags/cachyos"><i class="fas fa-tag" aria-hidden="true"></i> cachyos</a> <a class="tag" href="/tags/linux%20unplugged"><i class="fas fa-tag" aria-hidden="true"></i> linux unplugged</a> <a class="tag" href="/tags/linux%20podcast"><i class="fas fa-tag" aria-hidden="true"></i> linux podcast</a> <a class="tag" href="/tags/jupiter%20broadcasting"><i class="fas fa-tag" aria-hidden="true"></i> jupiter broadcasting</a> </div>')
    assert parse_tags('http://example.com','1','lup', ShowDetails(
        show_rss='https://serve.podhome.fm/rss/55b53584-4219-4fb0-b916-075ce23f714e',
        show_url='https://www.thisweekinbitcoin.show/',
        jb_url='https://www.jupiterbroadcasting.com/show/this-week-in-bitcoin',
        acronym='twib',
        name='This Week In Bitcoin',
        host_platform='podhome')) == []

def test_parse_tags_failure(requests_mock):
    requests_mock.get('http://127.0.0.1', status_code=404, text=None)
    assert parse_tags('http://127.0.0.1','1','lup', ShowDetails(
        show_rss='https://serve.podhome.fm/rss/55b53584-4219-4fb0-b916-075ce23f714e',
        show_url='https://www.thisweekinbitcoin.show/',
        jb_url='https://www.jupiterbroadcasting.com/show/this-week-in-bitcoin',
        acronym='twib',
        name='This Week In Bitcoin',
        host_platform='fireside')) == []
    assert parse_tags('http://127.0.0.1','1','lup', ShowDetails(
        show_rss='https://serve.podhome.fm/rss/55b53584-4219-4fb0-b916-075ce23f714e',
        show_url='https://www.thisweekinbitcoin.show/',
        jb_url='https://www.jupiterbroadcasting.com/show/this-week-in-bitcoin',
        acronym='twib',
        name='This Week In Bitcoin',
        host_platform='fireside')) == []