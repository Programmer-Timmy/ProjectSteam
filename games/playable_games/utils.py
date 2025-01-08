import importlib


def get_playable_games():
    IMAGES = {
        'satisfactory_api': 'https://portfolio.timmygamer.nl/img/66fe973b40b0f7.53385927.jpg',
        'hangman': 'https://t4.ftcdn.net/jpg/02/62/24/45/360_F_262244537_RjHfRBucxPyo7o6QetIAQYpd5O3h6cEN.jpg',
        'flapy_bird': 'https://i.pinimg.com/originals/a0/10/96/a01096406d987a54c14d498a6b420960.png',
    }

    DESCRIPTIONS = {
        'satisfactory_api': 'A place to manage your Satisfactory servers.',
        'hangman': 'A classic word guessing game.',
        'flapy_bird': 'A clone of the popular Flappy Bird game.',
    }

    module = importlib.import_module('games.playable_games.urls')
    urlpatterns = getattr(module, 'urlpatterns').copy()

    urlpatterns.pop(0)  # Remove the index path
    games = []

    for url in urlpatterns:
        link = url.pattern._route.replace('/\Z', '').replace('^', '').replace('/', '')
        name = link.replace('_', ' ').title()
        games.append({
            'name': name,
            'url': "playable_games:" + link + ":index",
            'image_url': IMAGES.get(link, ''),
            'description': DESCRIPTIONS.get(link, ''),
        })

    return games
