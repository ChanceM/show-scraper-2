#!/usr/bin/env python3

import concurrent.futures
import sys
import re
import requests
import yaml
from bs4 import BeautifulSoup, NavigableString, Tag
from typing import Union, Optional, Dict, List
from pydantic import AnyHttpUrl
from frontmatter import Post, dumps
from html2text import html2text
from loguru import logger
from pathlib import Path

from models import Rss
from models.scraper import Settings
from models.config import ConfigData, ShowDetails
from models.episode import Episode, Chapters
from models.participant import Participant
from models.item import Item
from models.podcast import Person
from models.sponsor import Sponsor
from models.strategies.sponsor import FiresideSponsorParse, PodhomeSponsorParse, SponsorParser
from models.strategies.tag import FiresideTagParse, PodhomeTagParse, TagParser


# The sponsors' data is collected into this global when episode files are scraped.
# This data is saved to files files after the episode files have been created.
SPONSORS: Dict[str, Sponsor] = {}  # JSON filename as key (e.g. "linode.com-lup.json")

#
PARTICIPANTS: Dict[str, Participant] = {}

# Regex to strip Episode Numbers and information after the |
# https://regex101.com/r/gkUzld/
SHOW_TITLE_REGEX = re.compile(r"^(?:(?:Episode)?\s?[0-9]+:+\s+)?(.+?)(?:(\s+\|+.*)|\s+)?$")

global config
config = None

def get_plain_title(title: str) -> str:
    """
    Get just the show title, without any numbering etc
    """
    return SHOW_TITLE_REGEX.match(title)[1]

def get_podcast_chapters(chapters: Chapters) -> Optional[Chapters]:
    try:
        resp = requests.get(chapters.url)
        resp.raise_for_status()

        try:
            Chapters.model_validate_json(resp.text)
        except Exception as e:
            logger.warning('Invalid chapters JSON.\n'
                           f'{e}')

        return Chapters(**resp.json())
    except requests.HTTPError:
        # No chapters
        pass
    except AttributeError:
        return None

def get_canonical_username(username: Person) -> str:
    """
    Get the last path part of the url which is the username for the hosts and guests.
    Replace it using the `username_map` from config.
    """
    usernames_map = config.get("usernames_map")

    # Replace username if found in usernames_map or default to input username
    return next(filter(str.__instancecheck__,(key for key, list in usernames_map.items() if username.name in list)), username.name)

def parse_sponsors(page_url: AnyHttpUrl, episode_number: str, show: str, show_details: ShowDetails) -> List[str]:
    response = requests.get(page_url,)
    page_soup = BeautifulSoup(response.text, features="html.parser")


    match show_details.host_platform:
        case 'podhome':
            parse_strategy = PodhomeSponsorParse()
        case _:
            parse_strategy = FiresideSponsorParse()

    try:
        sp: SponsorParser = SponsorParser(page_soup, show_details, parse_strategy)
        sponsors = sp.run()
    except Exception as e:
        logger.warning(f"Failed to collect/parse sponsor data! # Show: {show} Ep: {episode_number}\n"
            f"{e}")
        sponsors = {}

    SPONSORS.update(sponsors)

    return list(map(lambda sponsor: sponsors[sponsor].shortname, sponsors))

def parse_tags(page_url: AnyHttpUrl, episode_number: str, show: str, show_details: ShowDetails) -> List[str]:
    response = requests.get(page_url,)
    page_soup = BeautifulSoup(response.text, features="html.parser")

    match show_details.host_platform:
        case 'podhome':
            parse_strategy = PodhomeTagParse()
        case _:
            parse_strategy = FiresideTagParse()

    try:
        tag_parser: TagParser = TagParser(page_soup, show_details, parse_strategy)
        tags = tag_parser.run()
    except Exception as e:
        logger.warning(f"Failed to collect/parse tags! # Show: {show} Ep: {episode_number}\n"
            f"{e}")
        tags = []

    return tags

def parse_episode_number(title: str) -> str:
    # return re.match(r'.*?(\d+):', title).groups()[0]
    return re.match(r'.*?((?:Pocket Office )?\d+):', title).groups()[0]


def build_episode_file(item: Item, show: str, show_details: ShowDetails):
    episode_string = item.podcast_episode.episode if item.podcast_episode else parse_episode_number(item.title)
    episode_number, episode_number_padded = (int(episode_string), f'{int(episode_string):04}') if episode_string.isnumeric() else tuple(("".join(re.findall(r'[A-Z\d]',episode_string)).lower(),))*2

    output_file = Path(Settings.DATA_DIR) / 'content' / 'show' / show / f'{episode_number_padded.replace("/","")}.md'

    if not Settings.LATEST_ONLY and output_file.exists():
        # Overwrite when IS_LATEST_ONLY mode is true
        logger.warning(f"Skipping saving `{output_file}` as it already exists")
        return

    sponsors = parse_sponsors(item.link, episode_number,show,show_details)
    tags = sorted(item.itunes_keywords.keywords) if item.itunes_keywords else parse_tags(item.link, episode_number,show,show_details)

    description_soup = BeautifulSoup(item.description, features="html.parser")
    for br in description_soup.select('br'):
        br.decompose()

    # Remove Sponsor Links found in the description
    for anchor in description_soup.select('ul > li > a[rel=nofollow]'):
        if anchor.parent == None:
            continue
        anchor.parent.decompose()

    links_label = description_soup.find('strong', string=re.compile(r'.*Links|Show.*',re.IGNORECASE))
    if links_label:
        episode_links = ''.join([str(i) for i in links_label.find_all_next(['strong','li'])])
        # TWIB Allow for affiliate links
        if links_label.text == 'Affiliate LINKS:':
            links_label.string.replace_with(links_label.text.title())
            episode_links = str(links_label) + episode_links
    else:
        episode_links = ''.join([str(i) for i in description_soup.find_all(['strong','li'])])
    episode_links = re.sub(r'</li><strong>','</li><br/><strong>',episode_links)

    item.description = str(episode_links)
    description_parts = []

    node = description_soup.find('strong')

    if node != None:
        node = parent if type(parent := node.parent) is Tag else node
        # handle twib ep10 - description / sponsor wrapped in p tag.
        if type(parent.previous) != NavigableString and parent.name != '[document]':
            description_parts.insert(0, parent.contents[0])
        while type((previous := node.previous)) is NavigableString:
            description_parts.insert(0, previous.text.strip())
            node = previous

    episode = Episode(
                show_slug=show,
                show_name=show_details.name,
                episode=episode_number,
                episode_padded=episode_number_padded,
                episode_guid=item.guid.guid,
                title=get_plain_title(item.title),
                description=item.itunes_subtitle.root if item.itunes_subtitle else ' '.join(description_parts),
                date=item.pubDate,
                tags=tags,
                hosts=list(map(get_canonical_username, list(filter(lambda person: person.role in Settings.Host_Roles, item.podcast_persons)))),
                guests=list(map(get_canonical_username, list(filter(lambda person: person.role in Settings.Guest_Roles, item.podcast_persons)))),
                sponsors=sponsors,
                podcast_duration=item.itunes_duration.root,
                podcast_file=item.enclosure.url,
                podcast_bytes=item.enclosure.length,
                podcast_chapters=get_podcast_chapters(item.podcast_chapters),
                podcast_alt_file=None,
                podcast_ogg_file=None,
                video_file=None,
                video_hd_file=None,
                video_mobile_file=None,
                youtube_link=None,
                jb_url=f'{show_details.jb_url}/{episode_number}',
                fireside_url=item.link,
                value=item.podcast_value,
                episode_links=html2text(item.description)
            )

    build_participants(item.podcast_persons)

    save_file(output_file, episode.get_hugo_md_file_content(), overwrite=Settings.LATEST_ONLY)

def build_participants(participants: List[Person]):
    for participant in list(filter(lambda person: person.role in [*Settings.Host_Roles, *Settings.Guest_Roles], participants)):
        canonical_username = get_canonical_username(participant)
        filename = f'{canonical_username}.md'

        PARTICIPANTS.update({
            filename: Participant(
                type='host' if participant.role in Settings.Host_Roles else 'guest',
                username=canonical_username,
                title=participant.name,
                homepage=str(participant.href) if participant.href else None,
                avatar=f'images/people/{canonical_username}.{str(participant.img).split(".")[-1]}' if participant.img else None
            )
        })

        if participant.img:
            save_avatar_img(participant.img,canonical_username, f'images/people/{canonical_username}.{str(participant.img).split(".")[-1]}')

def save_avatar_img(img_url: str, username: str, relative_filepath: str) -> None:
    """Save the avatar image only if it doesn't exist.

    Return the file path relative to the `static` folder.
    For example: "images/people/chris.jpg"
    """
    try:
        full_filepath = Path(Settings.DATA_DIR) / 'static' / relative_filepath

        # Check if file exist BEFORE the request. This is more efficient as it saves
        # time and bandwidth
        if full_filepath.exists():
            logger.warning(f"Skipping saving `{full_filepath}` as it already exists")
            return

        resp = requests.get(img_url)
        resp.raise_for_status()

        save_file(full_filepath, resp.content, mode="wb")
        logger.info(f"Saved file: {full_filepath}")

    except Exception:
        logger.exception("Failed to save avatar!\n"
                         f"  img_url: {img_url}"
                         f"  username: {username}")

def save_sponsors(executor: concurrent.futures.ThreadPoolExecutor) -> None:
    logger.info(">>> Saving the sponsors found in episodes...")
    sponsors_dir = Path(Settings.DATA_DIR) / 'content' / 'sponsors'
    futures = []
    for filename, sponsor in SPONSORS.items():
        futures.append(executor.submit(
            save_post_obj_file,
            filename, Post('',**sponsor.model_dump()), sponsors_dir, overwrite=True))

    # Drain all threads
    for future in concurrent.futures.as_completed(futures):
        future.result()
    logger.info(">>> Finished saving sponsors")

def save_participants(executor: concurrent.futures.ThreadPoolExecutor) -> None:
    logger.info(">>> Saving the participants found in episodes...")
    person_dir = Path(Settings.DATA_DIR) / 'content' / 'people'
    futures = []
    for filename, participant in PARTICIPANTS.items():
        futures.append(executor.submit(
            save_post_obj_file,
            filename, Post('',**participant.model_dump()), person_dir, overwrite=True))

    # Drain all threads
    for future in concurrent.futures.as_completed(futures):
        future.result()
    logger.info(">>> Finished saving participants")

def save_post_obj_file(filename: str, post_obj: Post, dest_dir: Path, overwrite: bool = False) -> None:
    data_dont_override = set(config.get("data_dont_override"))
    if Settings.LATEST_ONLY and filename in data_dont_override:
        logger.warning(f"Filename `{filename}` found in `data_dont_override`! Will not save to it.")
        overwrite = False

    file_path = dest_dir / filename
    save_file(file_path, dumps(post_obj), overwrite=overwrite)

def save_file(file_path: Path, content: Union[bytes,str], mode: str = "w", overwrite: bool = False) -> bool:
    if not overwrite and file_path.exists():
        logger.warning(f"Skipping saving `{file_path}` as it already exists")
        return False

    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, mode) as f:
        f.write(content)
    logger.info(f"Saved file: {file_path}")
    return True

def main():
    global config
    with open("config.yml") as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
        validated_config = ConfigData(shows=config['shows'], usernames_map=config['usernames_map'])


    for show, show_config in validated_config.shows.items():
        response = requests.get(show_config.show_rss)

        rss = Rss.from_xml(response.content)

        with concurrent.futures.ThreadPoolExecutor() as executor:

            futures = []
            for idx, item in enumerate(rss.channel.items):
                if Settings.LATEST_ONLY and idx >= Settings.LATEST_ONLY_EP_LIMIT:
                    logger.debug(f"Limiting scraping to only {Settings.LATEST_ONLY_EP_LIMIT} most"
                            " recent episodes")
                    break
                futures.append(executor.submit(
                    build_episode_file,
                    item,
                    show,
                    show_config))

            # Drain all threads
            for future in concurrent.futures.as_completed(futures):
                future.result()

            save_sponsors(executor)
            save_participants(executor)


if __name__ == "__main__":
    Settings = Settings()
    logger.remove()  # Remove default logger
    logger.add(sys.stderr, level=Settings.LOG_LVL)

    logger.info("🚀🚀🚀 SCRAPER STARTED! 🚀🚀🚀")
    main()
    logger.success("🔥🔥🔥 ALL DONE :) 🔥🔥🔥\n\n")
    exit(0)