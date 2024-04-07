#!/usr/bin/env python3

import concurrent.futures
import os
import sys
import re
from urllib.parse import urlparse
import requests
import yaml
from bs4 import BeautifulSoup, NavigableString
from typing import Union, Optional, Dict, List
from pydantic import AnyHttpUrl
from frontmatter import Post, dumps
from html2text import html2text
from loguru import logger

from models import Rss
from models.scraper import Settings
from models.config import ConfigData, ShowDetails
from models.episode import Episode
from models.item import Item
from models.episode import Chapters
from models.podcast import Person
from models.sponsor import Sponsor


# The sponsors' data is collected into this global when episode files are scraped.
# This data is saved to files files after the episode files have been created.
SPONSORS: Dict[str, Sponsor] = {}  # JSON filename as key (e.g. "linode.com-lup.json")

# Regex to strip Episode Numbers and information after the |
# https://regex101.com/r/gkUzld/
SHOW_TITLE_REGEX = re.compile(r"^(?:(?:Episode)?\s?[0-9]+:+\s+)?(.+?)(?:(\s+\|+.*)|\s+)?$")

global config
config = None

def makedirs_safe(directory):
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

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

def parse_sponsors(page_url: AnyHttpUrl, episode_number: int, show: str, show_details: ShowDetails) -> List[str]:
    response = requests.get(page_url,)
    page_soup = BeautifulSoup(response.text, features="html.parser")

    # Get Sponsors
    sponsor_tags = page_soup.find_all('strong', string='Sponsor:')

    if not sponsor_tags:
        logger.warning(f"No sponsors found for this episode. # Show: {show} Ep: {episode_number}")
        return []

    sponsors = []
    for sponsor in sponsor_tags:
        try:
            sponsor_link = sponsor.next_sibling.next_sibling

            # FIXME: eventually get around to do a more "official" solution
            # Very ugly but works. The goal is to get the hostname of the sponsor
            # link without the subdomain. It would fail on tlds like "co.uk". but I
            # don't think JB had any sponsors like that so it's fine.
            sponsor_slug = ".".join(urlparse(sponsor_link['href']).hostname.split(".")[-2:])
            shortname = f"{sponsor_slug}-{show_details.acronym}".lower()
            sponsors.append(shortname)

            filename = f"{shortname}.md"

            description = " ".join([sponsor_link.find_next('strong').text, sponsor_link.find_next('strong').next_sibling.text])

            if sponsor_link and not SPONSORS.get(filename):
                SPONSORS.update({
                    filename: Sponsor(
                        shortname=shortname,
                        title=sponsor_link.text.strip(),
                        description=description,
                        link=sponsor_link.get('href')
                    )
                })
        except Exception as e:
            logger.warning(f"Failed to collect/parse sponsor data! # Show: {show} Ep: {episode_number}\n"
                           f"{e}")
        except NavigableString:
            pass

    return sponsors

def parse_episode_number(title: str) -> str:
    # return re.match(r'.*?(\d+):', title).groups()[0]
    return re.match(r'.*?((?:Pocket Office )?\d+):', title).groups()[0]


def build_episode_file(item: Item, show: str, show_details: ShowDetails):
    episode_string = parse_episode_number(item.title)
    episode_number, episode_number_padded = (int(episode_string), f'{int(episode_string):04}') if episode_string.isnumeric() else tuple(("".join(re.findall(r'[A-Z\d]',episode_string)).lower(),))*2

    output_file = f"{Settings.DATA_DIR}/content/show/{show}/{episode_number_padded.replace('/','')}.md"

    if not Settings.LATEST_ONLY and os.path.isfile(output_file):
        # Overwrite when IS_LATEST_ONLY mode is true
        logger.warning(f"Skipping saving `{output_file}` as it already exists")
        return

    sponsors = []

    # Parse up to first strong to build a summary description
    description_soup = BeautifulSoup(item.description, features="html.parser")
    description_p1  = description_soup.find(string=re.compile(r'.*|(strong)')).text
    description = description_p1
    try:
        description_p2 = description_soup.find('strong').previous.previous.previous.text

        if not description_p1 == description_p2:
            description += description_p2
    except:
        pass

    episode = Episode(
                show_slug=show,
                show_name=show_details.name,
                episode=episode_number,
                episode_padded=episode_number_padded,
                episode_guid=item.guid.guid,
                title=get_plain_title(item.title),
                description=item.itunesSubtitle.root if item.itunesSubtitle else description,
                date=item.pubDate,
                tags=[],
                hosts=list(map(get_canonical_username, list(filter(lambda person: person.role in Settings.Host_Roles, item.podcastPersons)))),
                guests=list(map(get_canonical_username, list(filter(lambda person: person.role in Settings.Guest_Roles, item.podcastPersons)))),
                sponsors=sponsors,
                podcast_duration=item.itunesDuration.root,
                podcast_file=item.enclosure.url,
                podcast_bytes=item.enclosure.length,
                podcast_chapters=get_podcast_chapters(item.podcastChapters),
                podcast_alt_file=None,
                podcast_ogg_file=None,
                video_file=None,
                video_hd_file=None,
                video_mobile_file=None,
                youtube_link=None,
                jb_url=f'{show_details.jb_url}/{episode_number}',
                fireside_url=item.link,
                value=item.podcastValue,
                episode_links=html2text(item.description)
            )

    save_file(output_file, episode.get_hugo_md_file_content(), overwrite=Settings.LATEST_ONLY)

def save_sponsors(executor):
    logger.info(">>> Saving the sponsors found in episodes...")
    sponsors_dir = os.path.join(Settings.DATA_DIR, "content", "sponsors")
    futures = []
    for filename, sponsor in SPONSORS.items():
        futures.append(executor.submit(
            save_post_obj_file,
            filename, Post('',**sponsor.model_dump()), sponsors_dir, overwrite=True))

    # Drain all threads
    for future in concurrent.futures.as_completed(futures):
        future.result()
    logger.info(">>> Finished saving sponsors")

def save_post_obj_file(filename: str, post_obj: Post, dest_dir: str, overwrite: bool = False) -> None:
    data_dont_override = set(config.get("data_dont_override"))
    if Settings.LATEST_ONLY and filename in data_dont_override:
        logger.warning(f"Filename `{filename}` found in `data_dont_override`! Will not save to it.")
        overwrite = False
    file_path = os.path.join(dest_dir, filename)
    save_file(file_path, dumps(post_obj), overwrite=overwrite)

def save_file(file_path: str, content: Union[bytes,str], mode: str = "w", overwrite: bool = False) -> bool:
    if not overwrite and os.path.exists(file_path):
        logger.warning(f"Skipping saving `{file_path}` as it already exists")
        return False

    makedirs_safe(os.path.dirname(file_path))
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

            futures.append

            # Drain all threads
            for future in concurrent.futures.as_completed(futures):
                future.result()

            save_sponsors(executor)


if __name__ == "__main__":
    Settings = Settings()
    logger.remove()  # Remove default logger
    logger.add(sys.stderr, level=Settings.LOG_LVL)

    logger.info("🚀🚀🚀 SCRAPER STARTED! 🚀🚀🚀")
    main()
    logger.success("🔥🔥🔥 ALL DONE :) 🔥🔥🔥\n\n")
    exit(0)