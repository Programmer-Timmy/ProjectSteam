$(document).ready(function () {
        const button = $('#advancedGameSettingsModal button[type="submit"]');
        const buttonText = button.find('#button-text');
        const spinner = button.find('.spinner-border');

        $('#advancedGameSettingsModal form').submit(function (e) {
                e.preventDefault();

                buttonText.text('Saving...');
                button.attr('disabled', true);
                spinner.removeClass('d-none');

                const form = $(this);
                const url = `/games/playable/satisfactory_api/updateAdvancedGameSettings/${server_id}/`;

                $.ajax({
                    type: 'POST',
                    url: url,
                    data: form.serialize(),
                    success: function (data) {
                        if (data.status === 'success') {
                            buttonText.text('Save');
                            spinner.addClass('d-none');
                            button.attr('disabled', false);
                            $('#advancedGameSettingsModal').modal('hide');

                            showMessageModal('success', 'Success', 'Server options have been updated.');

                        } else {
                            buttonText.text('Save');
                            spinner.addClass('d-none');
                            button.attr('disabled', false);
                            $('#advancedGameSettingsModal').modal('hide');

                            updateMessageModal('error', 'Error', 'An error occurred. Please try again.');
                        }
                    },
                    error: function () {
                        buttonText.text('Save');
                        spinner.addClass('d-none');
                        button.attr('disabled', false);
                        $('#advancedGameSettingsModal').modal('hide');

                        showMessageModal('error', 'Error', 'An error occurred. Please try again.');
                    }
                });
            });
        });

    function updateAdvancedGameSettings(advancedGameSettings) {
        $('#advancedGameSettingsModal form').html('');
        for (const value of advancedGameSettings) {
            let input;
            if (value.input_type === 'checkbox') {
                input = `
                    <div class="mb-1">
                        <div class="form-check form-switch m-0">
                            <input class="form-check input" type="checkbox" id="${value.key}" name="${value.key}" ${value.value === 'True' ? 'checked' : ''}>
                            <label class="form-check-label" for="${value.key}">${value.name}</label>
                        </div>
                        <div id="${value.key}HelpBlock" class="form-text m-0">
                            ${value.description}
                        </div>
                    </div>
                `;
            } else if (value.input_type === 'time') {
                input = `
                    <div class="mb-3">
                        <label for="${value.key}" class="form-label
                        ">${value.name}</label>
                        <input type="time" class="form-control" id="${value.key}" name="${value.key}" value="${value.value || '00:00'}">
                        <div id="${value.key}HelpBlock" class="form-text">
                            ${value.description}
                        </div>
                    </div>
                `;
            } else if (value.input_type === 'range') {
                input = `
                    <div class="mb-3">
                        <label for="${value.key}" class="form-label
                        ">${value.name}</label>
                        <input type="range" class="form-range" id="${value.key}" name="${value.key}" value="${value.value}" min="${value.min}" max="${value.max}" step="${value.step}">
                        <div id="${value.key}HelpBlock" class="form-text m-0">
                            ${value.description}
                        </div>
                    </div>
                `;
            } else {
                input = `
                    <div class="mb-3">
                        <label for="${value.key}" class="form-label
                        ">${value.name}</label>
                        <input type="number" class="form-control" id="${value.key}" name="${value.key}" value="${value.value}" min="${value.min}" max="${value.max}" step="${value.step}">
                        <div id="${value.key}HelpBlock" class="form-text">
                            ${value.description}
                        </div>
                    </div>
                `;
            }
        }
    }