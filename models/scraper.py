from pydantic_xml import BaseXmlModel, RootXmlModel
from pydantic import ConfigDict
from typing import Set
from pydantic_settings import BaseSettings, SettingsConfigDict
from logging import INFO

class Settings(BaseSettings):
    # Limit scraping only the latest episodes of the show (executes the script much faster!)
    # Used with GitHub Actions to run on a daily schedule and scrape the latest episodes.
    LATEST_ONLY: bool = False
    LATEST_ONLY_EP_LIMIT: int = 5
    # Root dir where all the scraped data should to saved to.
    # The data save to this dir follows the directory structure of the Hugo files relative
    # to the root of the repo.
    # Could be set via env variable to use the Hugo root directory.
    # Any files that already exist in this directory will not be overwritten.
    DATA_DIR: str = './data'
    LOG_LVL: int = INFO
    Host_Roles: Set = {'Host', 'Co-Host'}
    Guest_Roles: Set = {'Guest'}
    Extras: str = 'Allow'

    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')



class ScraperBaseXmlModel(BaseXmlModel):
    def __init_subclass__(self, **kwargs):
        super().__init_subclass__(**kwargs)
        self.__xml_search_mode__ = 'unordered'

    model_config = ConfigDict(extras=Settings().Extras)

class ScraperRootXmlModel(RootXmlModel):

    model_config = ConfigDict(extras=Settings().Extras)


NSMAP = {
    'podcast': 'https://podcastindex.org/namespace/1.0',
    'itunes': 'http://www.itunes.com/dtds/podcast-1.0.dtd',
    'atom': 'http://www.w3.org/2005/Atom'
}