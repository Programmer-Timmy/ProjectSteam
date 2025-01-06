from datetime import datetime

import requests

from dashboard.models import GameSessions
from games.models import GameCategories, GameGenres, GamePlatforms, GameSteamspyTags


def update_game_with_steam_data(game, steam_data, steam_spy_data):
    """
    Updates a game object with data fetched from Steam and Steam Spy APIs.

    Args:
        game (Games): The game object to update.
        steam_data (dict): The data fetched from Steam API.
        steam_spy_data (dict): The data fetched from Steam Spy API.

    Returns:
        Games: The updated game object.
    """
    platforms = steam_data.get('platforms', {})
    release_date = steam_data.get('release_date', {}).get('date', '')

    # Format release date
    formatted_date = format_release_date(release_date)

    # Update game fields
    game.release_date = formatted_date
    game.steam_image = steam_data.get('header_image', '')
    game.description = steam_data.get('detailed_description', '')
    game.short_description = steam_data.get('short_description', '')
    game.price = steam_data.get('price_overview', {}).get('final', 0) / 100
    game.developer = steam_data.get('developers', [''])[0]
    game.publisher = steam_data.get('publishers', [''])[0]
    game.achievements = steam_data.get('achievements', {}).get('total', 0)
    game.positive_ratings = steam_spy_data.get('positive', 0)
    game.negative_ratings = steam_spy_data.get('negative', 0)
    game.owners = steam_spy_data.get('owners', '')
    game.median_playtime = steam_spy_data.get('median_playtime', 0)
    game.average_playtime = steam_spy_data.get('average_playtime', 0)
    game.required_age = steam_data.get('required_age', 0)

    # Update platform, genre, and category data
    game = update_game_platforms(game, platforms)
    game = update_game_genres(game, steam_data.get('genres', []))
    game = update_game_categories_and_tags(game, steam_data.get('categories', []))

    # Save the updated game data
    game.save()
    return game


def format_release_date(release_date):
    """
    Format the release date from Steam's format to YYYY-MM-DD.

    Args:
        release_date (str): The original release date string from Steam.

    Returns:
        str: The formatted release date.
    """
    date_obj = datetime.strptime(release_date, '%d %b, %Y')
    return date_obj.strftime('%Y-%m-%d')


def update_game_platforms(game, platforms):
    """
    Update the platforms associated with a game.

    Args:
        game (Games): The game object to update.
        platforms (dict): A dictionary containing the platforms for the game.

    Returns:
        Games: The updated game object.
    """
    for platform_name, is_supported in platforms.items():
        if is_supported:
            platform, created = GamePlatforms.objects.get_or_create(platform_name=platform_name)
            game.game_platform_links.get_or_create(platform=platform)
    return game


def update_game_genres(game, genres):
    """
    Update the genres associated with a game.

    Args:
        game (Games): The game object to update.
        genres (list): A list of genres associated with the game.

    Returns:
        Games: The updated game object.
    """
    for genre in genres:
        genre_obj, created = GameGenres.objects.get_or_create(genre_name=genre['description'])
        game.game_genre_links.get_or_create(genre=genre_obj)
    return game


def update_game_categories_and_tags(game, categories):
    """
    Update the categories and tags associated with a game.

    Args:
        game (Games): The game object to update.
        categories (list): A list of categories associated with the game.

    Returns:
        Games: The updated game object.
    """
    for category in categories:
        category_obj, created = GameCategories.objects.get_or_create(category_name=category['description'])
        tag_obj, created = GameSteamspyTags.objects.get_or_create(tag_name=category['description'])
        game.game_category_links.get_or_create(category=category_obj)
        game.game_tag_links.get_or_create(tag=tag_obj)
    return game


def get_sorted_unique_game_categories(game):
    """
    Get the sorted unique categories for a game.

    Args:
        game (Games): The game object.

    Returns:
        list: A sorted list of unique category names.
    """
    categories = [link.category.category_name for link in game.game_category_links.all()]
    return sorted(set(categories))


def get_sorted_unique_game_genres(game):
    """
    Get the sorted unique genres for a game.

    Args:
        game (Games): The game object.

    Returns:
        list: A sorted list of unique genre names.
    """
    genres = [link.genre.genre_name for link in game.game_genre_links.all()]
    return sorted(set(genres))


def get_sorted_unique_game_platforms(game):
    """
    Get the sorted unique platforms for a game.

    Args:
        game (Games): The game object.

    Returns:
        list: A sorted list of unique platform names.
    """
    platforms = [link.platform.platform_name for link in game.game_platform_links.all()]
    return sorted(set(platforms))


def get_sorted_unique_game_tags(game):
    """
    Get the sorted unique tags for a game.

    Args:
        game (Games): The game object.

    Returns:
        list: A sorted list of unique tag names.
    """
    tags = [link.tag.tag_name for link in game.game_tag_links.all()]
    return sorted(set(tags))

def get_available_years(user_id):
    """
    Get the available years for which the user has game data.

    Args:
        user_id (int): The ID of the user.

    Returns:
        list: A list of available years.
    """
    available_years = list(
        GameSessions.objects.filter(user_game__user__id=user_id)
        .values('start_timestamp__year')
        .distinct()
        .order_by('start_timestamp__year')
    )

    return [year['start_timestamp__year'] for year in available_years]