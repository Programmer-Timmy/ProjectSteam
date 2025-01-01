import os

import requests
from dotenv import load_dotenv


class SteamApi:

    def __init__(self):
        load_dotenv()

        self.STEAM_API_KEY = os.getenv('STEAM_API_KEY')

    def fetch_steam_recently_played_games(self, steam_id):
        url = f'https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={self.STEAM_API_KEY}&steamid={steam_id}'

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.RequestException as e:
            return

        if not data:
            return

        return data

    @staticmethod
    def fetch_steam_game_data(appid):
        """
        Fetch game data from Steam API based on the game's appid.

        Args:
            appid (int): The appid of the game to fetch data for.

        Returns:
            dict or None: Game data from Steam, or None if the request fails or data is unavailable.
        """
        app_url = f"https://store.steampowered.com/api/appdetails/?appids={appid}&l=en"

        try:
            response = requests.get(app_url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data:
                return data.get(str(appid), {}).get('data', None)
        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching Steam data for {appid}: {e}")

        return None



