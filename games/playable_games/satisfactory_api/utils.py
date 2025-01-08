import os
import re

from cryptography.fernet import Fernet
from django.shortcuts import render
from dotenv import load_dotenv
from satisfactory_api_client import SatisfactoryAPI, APIError
from satisfactory_api_client.data import MinimumPrivilegeLevel

from games.playable_games.satisfactory_api.models import SatisfactoryApi

# Load the key
def load_key():
    load_dotenv()
    return os.getenv('FERNET_KEY')


# Encrypt the password
def encrypt_password(password: str) -> str:
    key = load_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(password.encode())
    return encrypted_password.decode('utf-8')

# Decrypt the password
def decrypt_password(encrypted_password: str) -> str:
    key = load_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_password.encode())
    return decrypted_password.decode('utf-8')

def show_page_with_error(request, error):
    user_servers = get_user_servers(request)
    print(user_servers)
    return render(request, 'playable_games/satisfactory_api/index.html', {
        'page_title': 'Satisfactory API',
        'error': error,
        'name': request.POST.get('name'),
        'host': request.POST.get('ip'),
        'port': request.POST.get('port'),
        'user_servers': user_servers
    })

def get_user_servers(request):
    user_servers = SatisfactoryApi.objects.filter(user=request.user)
    for server in user_servers:
        api = SatisfactoryAPI(server.host, server.port)
        try:
            server.online = api.health_check().data.get('health', False) == 'healthy'
        except Exception as e:
            server.online = False

    return user_servers


def login_api(api, password_hash):
    password = decrypt_password(password_hash)
    if password:
        try:
            api.password_login(MinimumPrivilegeLevel.ADMINISTRATOR, password)
        except APIError as e:
            return False

    else:
        try:
            api.passwordless_login(MinimumPrivilegeLevel.ADMINISTRATOR)
        except Exception as e:
            return False

    return True

def check_if_exist_and_owner(id, user):
    exists = SatisfactoryApi.objects.filter(id=id, user=user).exists()
    if exists:
        is_owner = SatisfactoryApi.objects.get(id=id).user == user
        return is_owner
    return False

def server_is_online(id):
    server = SatisfactoryApi.objects.get(id=id)
    api = SatisfactoryAPI(server.host, server.port)
    try:
        return api.health_check().data.get('health', False) == 'healthy'
    except Exception as e:
        return False


def get_downloadable_game_saves(api):
    saveGames = []
    sessions = api.enumerate_sessions().data

    for session in sessions.get('sessions', []):
        count = 0
        for saveGame in session['saveHeaders']:
            saveGames.append({
                'sessionName': session['sessionName'],
                'saveName': saveGame['saveName'],
            })
            # stop after 3 save games
            if count == 2:
                break

            count += 1

    return saveGames


def reformat_server_options(server_options):
    server_options_descriptions = {
        'FG.DSAutoPause': 'Auto pause when no clients are connected',
        'FG.DSAutoSaveOnDisconnect': 'Auto save when clients disconnect',
        'FG.DisableSeasonalEvents': 'Disable seasonal events',
        'FG.AutosaveInterval': 'Interval (in seconds) for auto-saving',
        'FG.ServerRestartTimeSlot': 'Time slot for server restart',
        'FG.SendGameplayData': 'Send gameplay data to the server',
        'FG.NetworkQuality': 'Quality of network connection (1-3)'
    }

    orginized_server_options = []
    for key, value in server_options['serverOptions'].items():
        min_value = 0
        max_value = 100
        step = 1
        input_type = 'number'
        # if value is 'true' or 'false' then it is a boolean
        if value == 'True' or value == 'False':
            input_type = 'checkbox'
        elif key == 'FG.ServerRestartTimeSlot':
            input_type = 'time'
            value = str(value).replace(".", ":")
            digits = value.split(':')
            if len(digits[0]) == 1:
                digits[0] = '0' + digits[0]
            if len(digits[1]) == 1:
                digits[1] = '0' + digits[1]
            value = ':'.join(digits)

        elif key == 'FG.NetworkQuality':
            input_type = 'range'
            min_value = 1
            max_value = 3
            step = 1

        if key == 'FG.AutosaveInterval':
            value = int(float(value) / 60)
            min_value = 0
            max_value = 120
            step = 1

        name = key.replace('FG.', '').replace('DS', ' ')

        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
        name = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', name)

        orginized_server_options.append({
            'key': key,
            'name': name,
            'value': value,
            'description': server_options_descriptions.get(key, ''),
            'input_type': input_type,
            'min': min_value,
            'max': max_value,
            'step': step
        })

    orginized_server_options.sort(key=lambda x: x['input_type'], reverse=True)

    return orginized_server_options


def reformat_advanced_game_settings(advanced_game_settings):
    descriptions = {
        "creativeModeEnabled": "Enables the use of all the settings below.",
        "FG.GameRules.NoPower": "Disables the requirement for power to operate buildings and machines.",
        "FG.GameRules.StartingTier": "Specifies the starting technology tier for new games. Default is 0.",
        "FG.GameRules.DisableArachnidCreatures": "Prevents arachnid creatures from spawning in the game.",
        "FG.GameRules.NoUnlockCost": "Removes costs for unlocking tiers, recipes, or schematics.",
        "FG.GameRules.SetGamePhase": "Defines the current phase of the game. Phase 3 is typical for advanced gameplay.",
        "FG.GameRules.GiveAllTiers": "Automatically unlocks all technology tiers.",
        "FG.GameRules.UnlockAllResearchSchematics": "Unlocks all research schematics in the M.A.M. (Molecular Analysis Machine).",
        "FG.GameRules.UnlockInstantAltRecipes": "Instantly unlocks all alternate recipes.",
        "FG.GameRules.UnlockAllResourceSinkSchematics": "Unlocks all rewards available in the Resource Sink.",
        "FG.GameRules.GiveItems": "Specifies the starting inventory for the player. Default is 'Empty'.",
        "FG.PlayerRules.NoBuildCost": "Allows construction without consuming resources.",
        "FG.PlayerRules.GodMode": "Enables God Mode, making the player invincible.",
        "FG.PlayerRules.FlightMode": "Allows the player to fly around the world.",
    }

    orginized_advanced_game_settings = []

    orginized_advanced_game_settings.append({
        'key': 'creativeModeEnabled',
        'name': 'Creative Mode',
        'value': advanced_game_settings['creativeModeEnabled'],
        'description': descriptions.get('creativeModeEnabled', ''),
        'input_type': 'checkbox'
    })

    for key, value in advanced_game_settings['advancedGameSettings'].items():
        if key == 'FG.GameRules.GiveItems':
            continue

        if value == 'True' or value == 'False':
            input_type = 'checkbox'
        else:
            input_type = 'number'

        name = key.replace('FG.GameRules.', '').replace('FG.PlayerRules.', ' ')

        name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
        name = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', name)

        orginized_advanced_game_settings.append({
            'key': key,
            'name': name,
            'value': value,
            'description': descriptions.get(key, ''),
            'input_type': input_type
        })

    orginized_advanced_game_settings.sort(key=lambda x: x['input_type'], reverse=True)

    return orginized_advanced_game_settings
