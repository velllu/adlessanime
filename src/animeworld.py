from flask import Flask, render_template
from flask import request
from dataclasses import dataclass
from typing import Any, List, Tuple, cast
import bs4, requests, webbrowser

from common import Episode, EpisodeData, url_to_soup, Source, Anime

url = "https://www.animeworld.so"
search_url = "/search?keyword="
play_url = "/play/"

class AnimeWorld(Source):
    def get_search(self, title: str) -> List[Anime]:
        animes: List[Anime] = []
        soup = url_to_soup(url + search_url + title)

        # This contains every anime
        container = cast(bs4.Tag, soup.select_one("div.film-list"))

        for anime in container.select("div.item"):
            image = cast(bs4.Tag, anime.find("img"))

            anime_title: str = str(image.get("alt"))
            anime_image: str = str(image.get("src"))

            anime_link: str = str(cast(bs4.Tag, anime.find("a")).get("href"))
            anime_id = anime_link.split(play_url)[1]

            animes.append(Anime(anime_title, anime_id, anime_image))

        return animes

    def get_episodes(self, anime_id: str) -> EpisodeData:
        episodes: List[Episode] = []

        soup = url_to_soup(url + play_url + anime_id)
        container = cast(bs4.Tag, soup.select_one("div.server.active"))

        # Getting episodes
        for episode in container.select("li.episode"):
            hyperlink = cast(bs4.Tag, episode.find("a"))
            link = str(hyperlink.get("href"))

            title = hyperlink.get_text()
            id = link.split(play_url + anime_id + "/")[1]

            episodes.append(Episode(title, id))

        # Getting description and image
        description = cast(bs4.Tag, soup.select_one("div.desc")).get_text()

        image_container = cast(bs4.Tag, soup.select_one("div#thumbnail-watch"))
        image = str(cast(bs4.Tag, image_container.find("img")).get("src"))

        return EpisodeData(episodes, description, image)

    def get_video_url(self, anime_id: str, episode_id: str) -> str:
        video_url: str = ""
        soup = url_to_soup(url + play_url + anime_id + "/" + episode_id)

        download_link = cast(bs4.Tag, soup.select_one("a#downloadLink"))
        video_link = str(download_link.get("href"))

        # We need to remove part of the link to skip a download page and directly get to
        # the video file
        video_link = video_link.replace("download-file.php?id=", "")

        return video_link
