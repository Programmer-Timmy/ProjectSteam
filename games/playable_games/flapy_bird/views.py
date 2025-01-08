from django.shortcuts import render


def hangman(request):
    return render(request, "playable_games/flapy_bird/index.html", {
        'page_title': 'Flapy Bird',
        'show_footer': False
    })
