import os

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
        server.online = api.health_check().data.get('health', False) == 'healthy'

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