import os
import io

from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv
from satisfactory_api_client import SatisfactoryAPI, APIError
from satisfactory_api_client.data import MinimumPrivilegeLevel, ServerOptions, AdvancedGameSettings

from games.playable_games.satisfactory_api.models import SatisfactoryApi
from games.playable_games.satisfactory_api.utils import show_page_with_error, encrypt_password, get_user_servers, \
    login_api, check_if_exist_and_owner, server_is_online, get_downloadable_game_saves, reformat_server_options, \
    reformat_advanced_game_settings

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

        return redirect('playable_games:satisfactory_api:index')


def satisfactory_api_details(request, id):
    if check_if_exist_and_owner(id, request.user):

        if server_is_online(id):
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
            server_options = reformat_server_options(api.get_server_options().data)
            advanced_game_settings = reformat_advanced_game_settings(api.get_advanced_game_settings().data)
            online = health.data.get('health', False)
        else:
            online = False
            server_data = {
                "activeSessionName": "No active session",
                "numConnectedPlayers": 0,
                "playerLimit": 4,
                "techTier": "Unknown",
                "gamePhase": "Unknown",
                "isGameRunning": False,
                "IsGamePaused": True,
                "totalGameDuration": "Unknown",
                "averageTickRate": "Unknown"
            }
            downloadable_game_saves = None
            server_options = None
            advanced_game_settings = None

        return render(request, 'playable_games/satisfactory_api/dashboard.html', {
            'page_title': 'Satisfactory API Dashboard',
            'online': online,
            'server_data': server_data,
            'saveGames': downloadable_game_saves,
            'serverOptions': server_options,
            'advancedGameSettings': advanced_game_settings,
            'id': id
        })

    return redirect('playable_games:satisfactory_api')


def download_satisfactory_api(request, id, save_name):
    # check if send by ajax
    if not request.method == 'GET':
        return render(request, '404.html', status=404)

    if check_if_exist_and_owner(id, request.user) and server_is_online(id):
        api_data = SatisfactoryApi.objects.get(id=id)
        api = SatisfactoryAPI(api_data.host, api_data.port)
        login_api(api, api_data.password_hash)

        saveGame = api.download_save_game(save_name)

        if saveGame:
            return FileResponse(io.BytesIO(saveGame.data), as_attachment=True, filename=save_name + '.sav')
        else:
            # django 404 page
            return render(request, '404.html', status=404)

    return redirect('playable_games:satisfactory_api')

def update_satisfactory_api(request, id):
    if check_if_exist_and_owner(id, request.user) and server_is_online(id):
        if request.method == 'POST':
            api_data = SatisfactoryApi.objects.get(id=id)
            api = SatisfactoryAPI(api_data.host, api_data.port)
            login_api(api, api_data.password_hash)

            try:
                serverOptions = ServerOptions(
                    DSAutoPause=request.POST.get('FG.DSAutoPause') == 'on',
                    DSAutoSaveOnDisconnect=request.POST.get('FG.DSAutoSaveOnDisconnect') == 'on',
                    AutosaveInterval=int(request.POST.get('FG.AutosaveInterval')) * 60,
                    ServerRestartTimeSlot=request.POST.get('FG.ServerRestartTimeSlot').replace(":", "."),
                    SendGameplayData=request.POST.get('FG.SendGameplayData') == 'on',
                    NetworkQuality=int(request.POST.get('FG.NetworkQuality'))
                )
                data = api.apply_server_options(serverOptions)
                if not data.success:
                    return JsonResponse({'status': 'failed', 'message': 'Failed to update server settings'}, status=400)

                return JsonResponse({'status': 'success', 'message': 'Server settings updated'}, status=200)
            except APIError as e:
                return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)


    return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)

def update_advanced_game_settings(request, id):
    if check_if_exist_and_owner(id, request.user) and server_is_online(id):
        if request.method == 'POST':
            api_data = SatisfactoryApi.objects.get(id=id)
            api = SatisfactoryAPI(api_data.host, api_data.port)
            login_api(api, api_data.password_hash)

            try:
                advanced_game_settings = AdvancedGameSettings(
                    NoPower=request.POST.get('FG.GameRules.NoPower'),
                    DisableArachnidCreatures=request.POST.get('FG.GameRules.DisableArachnidCreatures'),
                    NoUnlockCost=request.POST.get('FG.GameRules.NoUnlockCost'),
                    SetGamePhase=int(request.POST.get('FG.GameRules.SetGamePhase')),
                    GiveAllTiers=request.POST.get('FG.GameRules.GiveAllTiers'),
                    UnlockAllResearchSchematics=request.POST.get('FG.GameRules.UnlockAllResearchSchematics'),
                    UnlockInstantAltRecipes=request.POST.get('FG.GameRules.UnlockInstantAltRecipes'),
                    UnlockAllResourceSinkSchematics=request.POST.get('FG.GameRules.UnlockAllResourceSinkSchematics'),
                    GiveItems=request.POST.get('FG.GameRules.GiveItems'),
                    NoBuildCost=request.POST.get('FG.PlayerRules.NoBuildCost'),
                    GodMode=request.POST.get('FG.PlayerRules.GodMode'),
                    FlightMode=request.POST.get('FG.PlayerRules.FlightMode')
                )

                data = api.apply_advanced_game_settings(advanced_game_settings)

                if not data.success:
                    return JsonResponse({'status': 'failed', 'message': 'Failed to update advanced game settings'}, status=400)

                return JsonResponse({'status': 'success', 'message': 'Advanced game settings updated'}, status=200)
            except APIError as e:
                return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)

def shutdown_server(request, id):
    if check_if_exist_and_owner(id, request.user) and server_is_online(id):
        if request.method == 'POST':
            api_data = SatisfactoryApi.objects.get(id=id)
            api = SatisfactoryAPI(api_data.host, api_data.port)
            login_api(api, api_data.password_hash)

            try:
                data = api.shutdown()
                if not data.success:
                    return JsonResponse({'status': 'failed', 'message': 'Failed to shutdown server'}, status=400)

                return JsonResponse({'status': 'success', 'message': 'Server is shutting down'}, status=200)
            except APIError as e:
                return JsonResponse({'status': 'failed', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)


def get_server_info(request, id):
    if check_if_exist_and_owner(id, request.user):
        if not server_is_online(id):
            return JsonResponse({
                'online': False,
                'server_data': {
                "activeSessionName": "No active session",
                "numConnectedPlayers": 0,
                "playerLimit": 4,
                "techTier": "Unknown",
                "gamePhase": "Unknown",
                "isGameRunning": False,
                "IsGamePaused": True,
                "totalGameDuration": "Unknown",
                "averageTickRate": "Unknown"
            },
                'serverOptions': None,
                'advancedGameSettings': None,
                'saveGames': None
            })

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

        return JsonResponse({
            'online': health.data.get('health', False),
            'server_data': server_data,
            'serverOptions': reformat_server_options(api.get_server_options().data),
            'advancedGameSettings': reformat_advanced_game_settings(api.get_advanced_game_settings().data),
            'saveGames': get_downloadable_game_saves(api)
        })

    return JsonResponse({'status': 'failed', 'message': 'Invalid request'}, status=400)