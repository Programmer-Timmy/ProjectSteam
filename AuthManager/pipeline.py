import os

from django.shortcuts import redirect
from dotenv import load_dotenv
from social_core.exceptions import AuthException
from openid.consumer.consumer import SuccessResponse
import requests
from social_django.models import UserSocialAuth

from controlers.User import UserManager

load_dotenv()

STEAM_API_KEY = os.getenv('STEAM_API_KEY')

def fetch_steam_data(steam_id):
    """Fetch the user's Steam profile data using the Steam Web API."""
    url = f'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steam_id}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)

        data = response.json()
        if 'response' in data and 'players' in data['response'] and data['response']['players']:
            return data['response']['players'][0]
        else:
            print(f"No player data found for Steam ID: {steam_id}")
            return None  # No player data found
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Steam data for Steam ID {steam_id}: {e}")
        return None


def create_or_update_user(strategy, details, backend, user=None, *args, **kwargs):
    is_new = False

    extra_data = kwargs.get('response', None)

    if not extra_data:
        raise AuthException('No response data available')

    if isinstance(extra_data, SuccessResponse):
        ns_uri = 'http://specs.openid.net/auth/2.0'
        ns_key = 'claimed_id'

        if extra_data.isSigned(ns_uri, ns_key):
            claimed_id = extra_data.getSigned(ns_uri, ns_key)
            if claimed_id:
                steam_id = claimed_id.split('/')[-1]
            else:
                raise AuthException('Claimed ID is missing in the response')
        else:
            raise AuthException('claimed_id field is not signed in the response')
    else:
        raise AuthException('Invalid response data format')

    # Fetch Steam profile data
    steam_data = fetch_steam_data(steam_id)
    if not steam_data:
        raise AuthException(f'Unable to fetch Steam data for Steam ID: {steam_id}')

    # Save or update the user with the Steam data
    if user:
        print("Updating user with Steam data")
        if steam_id != user.steam_id:
            is_new = True

        user.steam_id = steam_id
        user.avatar_url = steam_data.get('avatarfull', '')
        user.steam_username = steam_data.get('personaname', '')
        user.save()

        if is_new:
            if not UserSocialAuth.objects.filter(user=user, provider='steam').exists():
                UserSocialAuth.objects.create(
                    user=user,
                    provider='steam',
                    uid=user.steam_id  # Make sure `steam_id` is populated
                )

            try:
                UserManager().update_steam_games(user)
                return redirect('steam_connected')
            except Exception as e:
                print(f"Error updating Steam games for user {user}: {e}")


        return {'is_new': False, 'user': user}

    return redirect('need_account')

