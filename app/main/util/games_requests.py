import asyncio

import requests
import requests_cache

GAMES_ARCHIVE_URL = "https://api.chess.com/pub/player/{username}/games/archives"


class GamesClient:
    def __init__(self):
        requests_cache.install_cache('test_cache', backend='sqlite')

    def get_all_games(self, username):
        requests_cache.clear()
        game_archive_urls = requests.get(GAMES_ARCHIVE_URL.replace("{username}", username)).json()["archives"]
        return asyncio.run(self.__get_games_async(game_archive_urls))

    @staticmethod
    def get_all_games_from_cache(username):
        game_archive_urls = requests.get(GAMES_ARCHIVE_URL.replace("{username}", username)).json()["archives"]
        return asyncio.run(GamesClient.__get_games_async(game_archive_urls))

    @staticmethod
    async def __get_games_async(urls):
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        session = requests.Session()
        session.mount('http://', adapter)
        with session as session:
            loop = asyncio.get_event_loop()
            tasks = [loop.run_in_executor(None, GamesClient.__fetch, session, url) for url in urls]
            return await asyncio.gather(*tasks)

    @staticmethod
    def __fetch(session, url):
        with session.get(url) as response:
            return response.json()["games"]
