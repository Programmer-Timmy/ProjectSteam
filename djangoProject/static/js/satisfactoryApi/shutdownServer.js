$(document).ready(function () {
        const shutdownButton = $('#confirmShutdownButton');
        const modalTitle = $('#messageModalLabel');
        const modalText = $('#messageModal .modal-body p');

        shutdownButton.on('click', function () {
            // Disable button to prevent multiple clicks
            shutdownButton.attr('disabled', true).html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Shutting Down...');

            // Define the shutdown URL
            const url = `/games/playable/satisfactory_api/shutdownServer/${server_id}/`;
            const serverButtons = $('#server_buttons button');

            $.ajax({
                type: 'POST',
                url: url,
                headers: { 'X-CSRFToken': csrftoken },
                success: function (data) {
                    if (data.status === 'success') {
                        $('#shutdownModal').modal('hide');

                        showMessageModal('success', 'Success', 'The server has been shut down.');
                        $('#offline').removeClass('d-none');
                        $('#online').addClass('d-none');
                        serverButtons.attr('disabled', true);

                        shutdownButton.attr('disabled', false).html('<i class="bi bi-power"></i> Confirm Shutdown');
                    } else {
                        handleShutdownError();
                    }
                },
                error: handleShutdownError
            });

            function handleShutdownError() {
                $('#shutdownModal').modal('hide');

                updateMessageModal('error', 'Error', 'An error occurred. Please try again.');
                shutdownButton.attr('disabled', false).html('<i class="bi bi-power"></i> Confirm Shutdown');
            }
        });
    });