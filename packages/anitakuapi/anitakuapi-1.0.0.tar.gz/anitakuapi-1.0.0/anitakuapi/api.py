import requests


class AnitakuapiX:
    """## AnitakuapiX

    Python wrapper for the Anitakuapi

    - Base Url : anitakuapi-87ab1094388c.herokuapp.com
    - Documentation : [Click Here](https://anitakuapi-87ab1094388c.herokuapp.com/docs)
    - Updates Channel : [TechZBots](https://telegram.me/zz)
    - Support Group : [TechZBots Support](https://telegram.me/zzx)
    """

    class Gogo:
        """
        ### GogoAnime Api
        """

        def __init__(self) -> None:
            self.base = "https://anitakuapi-87ab1094388c.herokuapp.com"

        def latest(self, page=1):
            """
            Get latest releases from GogoAnime

            - page : Page number (Default : 1)
            """
            data = requests.get(
                f"{self.base}/gogo/latest?page={page}"
            ).json()
            return data["results"]

        def anime(self, anime):
            """
            Get anime details from GogoAnime

            - anime : Anime id
            """
            data = requests.get(
                f"{self.base}/gogo/anime?id={anime}"
            ).json()
            return data["results"]

        def search(self, query):
            """
            Search anime from GogoAnime

            - query : Anime name
            """
            data = requests.get(
                f"{self.base}/gogo/search/?query={query}"
            ).json()
            return data["results"]

        def episode(self, episode, lang="sub"):
            """
            Get episode links from GogoAnime (Download And Stream Links)

            - episode : Episode id, Ex : horimiya-dub-episode-3
            - lang : sub or dub or both
            """
            data = requests.get(
                f"{self.base}/gogo/episode?id={episode}&lang={lang}"
            ).json()["results"]
            return data

        def stream(self, url):
            """
            Get m3u8 stream links from GogoAnime

            - url : Episode url"""
            url = str(requests.utils.quote(url))
            data = requests.get(
                f"{self.base}/gogo/stream?url={url}"
            ).json()
            return data["results"]
