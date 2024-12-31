"""
This script is used to retrieve the last played games from the Steam API for all users who have a Steam ID and have not opted out.
"""

import os
from datetime import timedelta

import requests
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from dotenv import load_dotenv

from dashboard.models import GameSessions, Games

User = get_user_model()

load_dotenv()

STEAM_API_KEY = os.getenv('STEAM_API_KEY')

class Command(BaseCommand):
    help = 'Retrieve all users with a Steam ID and opt-out set to False'

    def handle(self, *args, **kwargs):
        # Query users
        self.stdout.write("Fetching data from Steam API...")
        users = User.objects.filter(steam_id__isnull=False, steam_opt_out=False)

        if not users.exists():
            self.stdout.write(self.style.WARNING("No users found with the specified criteria."))
            return

        # get last played games from steam api
        for user in users:
            # getting last palayed games in the last 2 weeks form the databavse
            last_played_games_in_db = GameSessions.objects.filter(user_game__user=user, start_timestamp__gte=timezone.now() - timedelta(weeks=2)).order_by('-start_timestamp')

            last_played_games_in_db = last_played_games_in_db.values('user_game__app__appid').annotate(total_time=Sum('total_time'))

            print(last_played_games_in_db)

            url = f'https://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v1/?key={STEAM_API_KEY}&steamid={user.steam_id}'

            data = None
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)

                data = response.json()
            except requests.exceptions.RequestException as e:
                self.stdout.write(f"Error fetching Steam data for Steam ID {user.steam_id}: {e}")
                continue

            if not data:
                continue

            else:
                for game in data['response']['games']:
                    # check if game exist in db
                    if not Games.objects.filter(appid=game['appid']).exists():
                        self.stdout.write(f"Game: {game['name']} not found in the database. Adding it now.")
                        Games.objects.create(
                            appid=game['appid'],
                            name=game['name'],
                        )

                    if not user.user_games.filter(app__appid=game['appid']).exists():
                        self.stdout.write(f"Game: {game['name']} not found in the user's games. Adding it now.")
                        user.user_games.create(
                            app=Games.objects.get(appid=game['appid']),
                            last_played=timezone.now(),
                            hours_played=game['playtime_forever'],
                        )

                    game_in_db = last_played_games_in_db.filter(user_game__app__appid=game['appid']).first()

                    if game_in_db:
                        game['playtime_2weeks'] = round(game['playtime_2weeks'] / 60, 2)
                        remaining_time = game['playtime_2weeks'] - game_in_db['total_time']
                        print(remaining_time)
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

        self.stdout.write(self.style.SUCCESS(f"Processed {users.count()} users successfully."))