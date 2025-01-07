function updateServerData() {
    $.get(`/games/playable/satisfactory_api/getServerInfo/${server_id}/`, function (data) {
            const serverData = data.server_data;
            const serverOptions = data.serverOptions;
            const advancedGameSettings = data.advancedGameSettings;
            const saveGames = data.saveGames;

            const online = data.online;
            const onlineElement = $('#online');
            const offlineElement = $('#offline');
            const serverButtons = $('#server_buttons button');

            if (online) {
                onlineElement.removeClass('d-none');
                offlineElement.addClass('d-none');
                serverButtons.attr('disabled', false);
            } else {
                onlineElement.addClass('d-none');
                offlineElement.removeClass('d-none');
                serverButtons.attr('disabled', true);
            }

            if (serverData === null) {
                return;
            }
            $('#server_data').html(`
                    <dt class="col-sm-4">Active Save Game:</dt>
                    <dd class="col-sm-8">${serverData.activeSessionName}</dd>

                    <dt class="col-sm-4">Player Count:</dt>
                    <dd class="col-sm-8">${serverData.numConnectedPlayers} / ${serverData.playerLimit}</dd>

                    <dt class="col-sm-4">Tier:</dt>
                    <dd class="col-sm-8">${serverData.techTier}</dd>

                    <dt class="col-sm-4">Game Phase:</dt>
                    <dd class="col-sm-8">${serverData.gamePhase}</dd>

                    <dt class="col-sm-4">Is Game Running:</dt>
                    <dd class="col-sm-8">
                        ${serverData.isGamePaused ? '<span class="text-danger">No</span>' : '<span class="text-success">Yes</span>'}
                    </dd>

                    <dt class="col-sm-4">Total Duration:</dt>
                    <dd class="col-sm-8">${serverData.totalGameDuration}</dd>

                    <dt class="col-sm-4">Tick Rate:</dt>
                    <dd class="col-sm-8">${serverData.averageTickRate} ticks/s</dd>
                `);

            updateSaveGames(saveGames);
            updateServerOptions(serverOptions);
            updateAdvancedGameSettings(advancedGameSettings);
        }
    );
}

$(document).ready(function () {
    setInterval(updateServerData, 60000);
});
