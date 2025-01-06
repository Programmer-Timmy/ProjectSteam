import requests

class SteamSpyApi:

    @staticmethod
    def get_steam_games(page: int = 1):
        try:
            url = f"https://steamspy.com/api.php?request=all&page={page}"
            response = requests.get(url)
            if response.status_code == 500:
                return

            response.raise_for_status()
            page_data = response.json()

            if not page_data:
                return

            return page_data

        except requests.exceptions.RequestException as e:
            return

    @staticmethod
    def get_steam_game_data(appid) -> dict | None:
        """
        Fetch game data from Steam Spy API based on the game's appid.

        Args:
            appid (int): The appid of the game to fetch data for.

        Returns:
            dict or None: Game data from Steam Spy, or None if the request fails or data is unavailable.
        """
        try:
            app_url = f"https://steamspy.com/api.php?request=appdetails&appid={appid}"
            response = requests.get(app_url, timeout=10)
            response.raise_for_status()  # Raises an error for bad responses
            data = response.json()

            if data:
                return data
        except (requests.RequestException, ValueError) as e:
            print(f"Error fetching Steam Spy data for {appid}: {e}")

        return None
