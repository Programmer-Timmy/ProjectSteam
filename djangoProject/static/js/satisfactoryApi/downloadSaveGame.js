var downloadButton = $('#downloadModal button[type="submit"]');

$('#downloadModal form').submit(function (e) {
    e.preventDefault(); // Prevent default form submission

    downloadButton.prop('disabled', true);
    downloadButton.find('#button-text').text('Downloading...');
    const saveGame = $('#game_session').val();

    if (!saveGame) {
        alert('Please select a save game to download.');
        downloadButton.prop('disabled', false);
        downloadButton.find('#button-text').text('Download');
        return;
    }
    const csrfToken = $('input[name="csrfmiddlewaretoken"]').val();
    downloadButton.find('.spinner-border').removeClass('d-none');
    const url = `../download/${server_id}/${saveGame}/?csrfmiddlewaretoken=${csrfToken}`;

    $.get(url, function (data, textStatus, xhr) {
        if (xhr.status === 200) {
            const blob = new Blob([data], {type: 'application/octet-stream'});
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = saveGame + '.sav';
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);

            // Close the modal
            $('#downloadModal').modal('hide');
            showMessageModal('success', 'Success', 'Save game has been downloaded.');

        } else {
            // Handle errors
            showMessageModal('error', 'Error', 'An error occurred while downloading the save game.');
        }

        downloadButton.html('Download');
        downloadButton.prop('disabled', false);
        downloadButton.find('.spinner-border').addClass('d-none');
    }).fail(function () {
        downloadButton.html('Download');
        downloadButton.prop('disabled', false);
        downloadButton.find('.spinner-border').addClass('d-none');
        showMessageModal('error', 'Error', 'An error occurred while downloading the save game.');
    });
});

function updateSaveGames(saveGames) {
    const gameSessionSelect = $('#game_session');
    gameSessionSelect.empty();
    gameSessionSelect.append('<option value="" disabled selected>Select a Game Save</option>');

    for (const gameSession of saveGames) {
        gameSessionSelect.append(`<option value="${gameSession.saveName}">${gameSession.saveName}</option>`);
    }
}