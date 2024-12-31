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

class Command(BaseCommand):
    help = 'Retrieve all users with a Steam ID and opt-out set to False'

    def handle(self, *args, **kwargs):
        # Query games
        self.stdout.write("Fetching data from SteamSPpy API...")
        page = 1
        data = {}
        while True:
            try:
                url = f"https://steamspy.com/api.php?request=all&page={page}"
                response = requests.get(url)
                if response.status_code == 500:
                    break

                response.raise_for_status()
                page_data = response.json()

                if not page_data:
                    break

                data.update(response.json())
                page += 1

            except requests.exceptions.RequestException as e:
                self.stdout.write(f"Error fetching Steam data: {e}")
                return

            if not data:
                self.stdout.write(self.style.WARNING("No data found."))
                return

        self.stdout.write(self.style.SUCCESS("Data fetched successfully."))

        total = len(data)
        completed = 0

        for steam_id, game in data.items():
            try:
                # overwrite the existing message
                # Check if the game exists in the database
                game_obj = Games.objects.filter(appid=steam_id).first()
                price = int(game['price']) / 100
                if not game_obj:
                    Games.objects.create(
                        appid=steam_id,
                        name=game['name'],
                        developer=game['developer'],
                        publisher=game['publisher'],
                        positive_ratings=game['positive'],
                        negative_ratings=game['negative'],
                        owners=game['owners'],
                        price=price,
                        steam_image=f"https://steamcdn-a.akamaihd.net/steam/apps/{steam_id}/header.jpg",
                    )
                else: # Update the game
                    game_obj.name = game['name']
                    game_obj.developer = game['developer']
                    game_obj.publisher = game['publisher']
                    game_obj.positive = game['positive']
                    game_obj.negative = game['negative']
                    game_obj.owners = game['owners']
                    game_obj.price = price
                    game_obj.save()
            except Exception as e:
                self.stdout.write(f"Error processing game {game['name']}: {e}")
                continue

            completed += 1
            self.stdout.write(f"Processing games... {completed}/{total}", ending='\r')

        self.stdout.write(self.style.SUCCESS(f"Processed {total} games successfully.", ending='\n'))
