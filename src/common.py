from typing import List, Tuple
from dataclasses import dataclass

import bs4
import requests

def url_to_soup(url: str) -> bs4.BeautifulSoup:
    return bs4.BeautifulSoup(requests.get(url).text, "html.parser")

@dataclass
class Anime:
    # example: Naruto Shippuden
    title: str

    # example: naruto-shippuden
    id: str

    # example: https://www.animestreamingexample.com/naruto-shippuden.png
    image: str 

@dataclass
class Episode:
    # example: 42, or sometimes when there are two episodes in one 42-43
    title: str

    id: str

@dataclass
class EpisodeData:
    episodes: List[Episode]
    description: str
    image: str

class Source:
    def get_search(self, title: str) -> List[Anime]:
        raise NotImplementedError

    # First str is the description, second str is 
    def get_episodes(self, anime_id: str) -> EpisodeData:
        raise NotImplementedError

    def get_video_url(self, anime_id: str, episode_id: str) -> str:
        raise NotImplementedError
