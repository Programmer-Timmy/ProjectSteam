"""
This script is used to retrieve the last played games from the Steam API for all users who have a Steam ID and have not opted out.
"""

import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv
from controlers.User import UserManager

User = get_user_model()

load_dotenv()

STEAM_API_KEY = os.getenv('STEAM_API_KEY')

class Command(BaseCommand):
    help = 'Retrieve all users with a Steam ID and opt-out set to False'

    def handle(self, *args, **kwargs):
        # Query users
        self.stdout.write("Fetching data from Steam API...")
        users = User.objects.filter(steam_id__isnull=False, steam_opt_out=False, opt_out=False)

        if not users.exists():
            self.stdout.write(self.style.WARNING("No users found with the specified criteria."))
            return

        # get last played games from steam api
        for user in users:
            # getting last palayed games in the last 2 weeks form the databavse
            UserManager(self.stdout, self.style).update_steam_games(user)
            UserManager(self.stdout, self.style).update_steam_user_data(user)

        self.stdout.write(self.style.SUCCESS(f"Processed {users.count()} users successfully."))