let limit = 30;
const search = $('#search');
const loadMore = $('#load-more');
const csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

function getGames(searchValue) {
    // save search data to url
    const url = new URL(window.location);
    url.searchParams.set('search', searchValue);
    url.searchParams.set('limit', limit);
    window.history.pushState({}, '', url);

    $.ajax({
        url: "/ajax/get_games/",
        type: "get",
        data: {
            csrfmiddlewaretoken: csrf_token,
            search: searchValue,
            order_by: 'appid',
            order: 'asc',
            limit: limit
        },
        success: function (data) {
            $('#games').html(data);
            loadMore.find('span').addClass('d-none')

            const games = $('#games .card');
            if (games.length < limit) {
                loadMore.addClass('d-none');
            } else {
                loadMore.removeClass('d-none');
            }
        }
    });
}

search.on('input', function () {
    const searchValue = search.val();
    limit = 30;
    getGames(searchValue);
});

loadMore.on('click', function () {
    limit += 30;
    loadMore.find('span').removeClass('d-none');
    getGames(search.val());
});