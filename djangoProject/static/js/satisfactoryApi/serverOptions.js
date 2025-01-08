$(document).ready(function () {
    const button = $('#serverOptionsModal button[type="submit"]');
    const buttonText = button.find('#button-text');
    const spinner = button.find('.spinner-border');

    $('#serverOptionsModal form').submit(function (e) {
        e.preventDefault();

        buttonText.text('Saving...');
        button.attr('disabled', true);
        spinner.removeClass('d-none');

        const form = $(this);
        const url = `/games/playable/satisfactory_api/updateSettings/${server_id}/`;

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function (data) {
                if (data.status === 'success') {
                    buttonText.text('Save');
                    spinner.addClass('d-none');
                    button.attr('disabled', false);
                    $('#serverOptionsModal').modal('hide');

                    showMessageModal('success', 'Success', 'Server options have been updated.');

                } else {
                    buttonText.text('Save');
                    spinner.addClass('d-none');
                    button.attr('disabled', false);
                    $('#serverOptionsModal').modal('hide');

                    updateMessageModal('error', 'Error', 'An error occurred. Please try again.');
                }
            },
            error: function () {
                buttonText.text('Save');
                spinner.addClass('d-none');
                button.attr('disabled', false);
                $('#serverOptionsModal').modal('hide');

                showMessageModal('error', 'Error', 'An error occurred. Please try again.');
            }
        });
    });
});

function updateServerOptions(serverOptions) {
    for (const option of serverOptions) {
        const element = $(`#${option.key}`);
        if (element.length === 0) {
            continue;
        }

        if (option.input_type === 'checkbox') {
            element.prop('checked', option.value === 'True');
        } else {
            element.val(option.value);
        }
    }
}