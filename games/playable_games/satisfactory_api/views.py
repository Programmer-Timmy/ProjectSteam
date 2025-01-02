import os
import io

from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv
from satisfactory_api_client import SatisfactoryAPI, APIError
from satisfactory_api_client.data import MinimumPrivilegeLevel

from djangoProject import settings
from games.playable_games.satisfactory_api.models import SatisfactoryApi
from games.playable_games.satisfactory_api.utils import show_page_with_error, encrypt_password, get_user_servers, \
    login_api, check_if_exist_and_owner

load_dotenv()
hash_key = os.getenv('HASH_KEY')
hash_salt = os.getenv('HASH_SALT')


def satisfactory_api(request):
    if request.method == 'GET' and 'delete' in request.GET:
        # check if owner
        exists = SatisfactoryApi.objects.filter(id=request.GET.get('delete'), user=request.user).exists()
        if exists:
            is_owner = SatisfactoryApi.objects.get(id=request.GET.get('delete')).user == request.user
            if is_owner:
                SatisfactoryApi.objects.get(id=request.GET.get('delete')).delete()

        return redirect('playable_games:satisfactory_api')

    if request.method == 'POST':
        name = request.POST.get('name')
        host = request.POST.get('ip')
        port = request.POST.get('port')
        token_type = MinimumPrivilegeLevel.ADMINISTRATOR
        password = request.POST.get('password')

        api = SatisfactoryAPI(host, port)

        if password:
            try:
                api.password_login(token_type, password)
            except APIError as e:
                return show_page_with_error(request, 'Wrong password or ip')

        else:
            try:
                api.passwordless_login(token_type)
            except Exception as e:
                return show_page_with_error(request, 'Wrong password or ip')

        if api.verify_authentication_token().success:
            h = encrypt_password(password)

            # hash the password
            SatisfactoryApi.objects.create(
                name=name,
                host=host,
                port=port,
                password_hash=h,
                user=request.user
            )

    user_servers = get_user_servers(request)

    return render(request, 'playable_games/satisfactory_api/index.html', {
        'page_title': 'Satisfactory API',
        'user_servers': user_servers
    })


def delete_satisfactory_api(request, id):
    if id:
        exists = SatisfactoryApi.objects.filter(id=id, user=request.user).exists()
        if exists:
            is_owner = SatisfactoryApi.objects.get(id=id).user == request.user
            if is_owner:
                SatisfactoryApi.objects.get(id=id).delete()

        return redirect('playable_games:satisfactory_api')


def satisfactory_api_details(request, id):
    if check_if_exist_and_owner(id, request.user):
        if request.method == 'POST' and request.POST.get('game_session'):
            return redirect('playable_games:satisfactory_api:satisfactory_api_download', id=id, save_name=request.POST.get('game_session'))

        api_data = SatisfactoryApi.objects.get(id=id)
        api = SatisfactoryAPI(api_data.host, api_data.port)
        login_api(api, api_data.password_hash)


        health = api.health_check()
        server_data = api.query_server_state().data['serverGameState']
        server_data['gamePhase'] = server_data['gamePhase'].split('/')[-1].split('.')[0].replace('_',
                                                                                                 ' ').replace(
            'GP ', '')
        server_data['totalGameDuration'] = str(server_data['totalGameDuration'] // 3600) + ' hours and ' + str(
            round(server_data['totalGameDuration'] % 3600 / 60)) + ' minutes'
        server_data['averageTickRate'] = str(round(server_data['averageTickRate']))

        downloadable_game_saves = get_downloadable_game_saves(api)
        return render(request, 'playable_games/satisfactory_api/dashboard.html', {
            'page_title': 'Satisfactory API Dashboard',
            'online': health.data.get('health', False),
            'server_data': server_data,
            'saveGames': downloadable_game_saves,
            'id': id
        })

    return redirect('playable_games:satisfactory_api')

def download_satisfactory_api(request, id, save_name):
    # check if send by ajax
    if not request.method == 'GET':
        return JsonResponse({'error': 'Not allowed'}, status=400)

    if check_if_exist_and_owner(id, request.user):
        api_data = SatisfactoryApi.objects.get(id=id)
        api = SatisfactoryAPI(api_data.host, api_data.port)
        login_api(api, api_data.password_hash)

        saveGame = api.download_save_game(save_name)

        if saveGame:
            return FileResponse(io.BytesIO(saveGame.data), as_attachment=True, filename=save_name + '.sav')
        else:
            return JsonResponse({'error': 'Save game not found'}, status=400)

    return JsonResponse({'error': 'Not allowed'}, status=400)

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
