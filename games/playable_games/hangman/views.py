from django.shortcuts import render


def hangman(request):
    return render(request, "playable_games/hangman/index.html", {
        'page_title': 'Hangman',
    })
