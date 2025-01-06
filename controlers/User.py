from datetime import timedelta
from django.db.models import Sum
from django.utils import timezone
from controlers.api.SteamApi import SteamApi
from dashboard.models import GameSessions
from games.models import Games


class UserManager:
    def __init__(self, stdout=None, style=None):
        """
        Initializes the User class.

        Parameters
        -------
        stdout : Optional
            Stream for writing output (e.g., console).
        style : Optional
            Style object for formatting output messages.
        -------
        """
        self.stdout = stdout
        self.style = style

    def update_steam_games(self, user):
        """
        Updates the Steam game data for a given user.

        Parameters
        -------
        user : User
            The user object whose Steam games need to be updated.
        -------
        """
        print("Fetching data from Steam API...")
        last_played_games_in_db = self._get_last_played_games(user)
        recently_played_games = SteamApi().fetch_steam_recently_played_games(user.steam_id)

        if not recently_played_games:
            self._handle_api_error(user)
            return

        self._process_recent_games(recently_played_games['response']['games'], user, last_played_games_in_db)

    def _get_last_played_games(self, user):
        """
        Retrieves games the user has played in the last two weeks from the database.

        Parameters
        -------
        user : User
            The user object.

        Returns
        -------
        QuerySet
            Aggregated game data grouped by app ID.
        -------
        """
        return (
            GameSessions.objects.filter(
                user_game__user=user,
                start_timestamp__gte=timezone.now() - timedelta(weeks=2)
            )
            .values('user_game__app__appid')
            .annotate(total_time=Sum('total_time'))
            .order_by('-total_time')
        )

    def _handle_api_error(self, user):
        """
        Handles errors encountered while fetching data from the Steam API.

        Parameters
        -------
        user : User
            The user object whose data could not be fetched.
        -------
        """
        if self.stdout:
            self.stdout.write(self.style.ERROR(f"Error fetching data for user: {user.username}"))
        else:
            raise Exception(f"Error fetching data for user: {user.username}")

    def _process_recent_games(self, games, user, last_played_games_in_db):
        """
        Processes the list of recently played games and updates the database.

        Parameters
        -------
        games : list
            List of games recently played by the user.
        user : User
            The user object.
        last_played_games_in_db : QuerySet
            Aggregated game data for the user from the database.
        -------
        """
        for game in games:
            self._add_game_to_db_if_missing(game)
            self._add_game_to_user_if_missing(game, user)
            self._update_game_sessions(game, user, last_played_games_in_db)

    def _add_game_to_db_if_missing(self, game):
        """
        Adds a game to the database if it does not already exist.

        Parameters
        -------
        game : dict
            Game data retrieved from the Steam API.
        -------
        """
        if not Games.objects.filter(appid=game['appid']).exists():
            if self.stdout:
                self.stdout.write(f"Game: {game['name']} not found in the database. Adding it now.")
            Games.objects.create(
                appid=game['appid'],
                name=game['name'],
                steam_image=f"https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/{game['appid']}/header.jpg"
            )

    def _add_game_to_user_if_missing(self, game, user):
        """
        Adds a game to the user's library if it does not already exist.

        Parameters
        -------
        game : dict
            Game data retrieved from the Steam API.
        user : User
            The user object.
        -------
        """
        if not user.user_games.filter(app__appid=game['appid']).exists():
            if self.stdout:
                self.stdout.write(f"Game: {game['name']} not found in the user's games. Adding it now.")
            user.user_games.create(
                app=Games.objects.get(appid=game['appid']),
                last_played=timezone.now(),
                hours_played=game['playtime_forever'],
            )

    def _update_game_sessions(self, game, user, last_played_games_in_db):
        """
        Updates the game session records in the database.

        Parameters
        -------
        game : dict
            Game data retrieved from the Steam API.
        user : User
            The user object.
        last_played_games_in_db : QuerySet
            Aggregated game data for the user from the database.
        -------
        """
        game_in_db = last_played_games_in_db.filter(user_game__app__appid=game['appid']).first()

        if game_in_db:
            game['playtime_2weeks'] = round(game['playtime_2weeks'] / 60, 2)
            remaining_time = round(max(0, (game['playtime_2weeks'] - game_in_db['total_time'])), 2)

            if remaining_time > 0:
                GameSessions.objects.create(
                    user_game=user.user_games.get(app__appid=game['appid']),
                    start_timestamp=timezone.now(),
                    end_timestamp=timezone.now(),
                    total_time=remaining_time,
                    ongoing=False
                )
        else:
            hours_played = round(game['playtime_2weeks'] / 60, 2)
            GameSessions.objects.create(
                user_game=user.user_games.get(app__appid=game['appid']),
                start_timestamp=timezone.now(),
                end_timestamp=timezone.now(),
                total_time=hours_played,
                ongoing=False
            )

    def _update_user_data(self, user, user_data):
        """
        Updates the user data in the database.

        Parameters
        -------
        user : User
            The user object.
        user_data : dict
            User data retrieved from the Steam API.
        -------
        """
        user.avatar_url = user_data['response']['players'][0]['avatarfull']
        user.steam_username = user_data['response']['players'][0]['personaname']
        user.save()


    def update_steam_user_data(self, user):
        """
        Updates the Steam user data for a given user.

        Parameters
        -------
        user : User
            The user object whose Steam user data needs to be updated.
        -------
        """
        user_data = SteamApi().fetch_steam_user_data(user.steam_id)

        if not user_data:
            self._handle_api_error(user)
            return

        self._update_user_data(user, user_data)
