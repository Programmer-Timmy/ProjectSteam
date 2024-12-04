from django.db import models

# new games model
class Games(models.Model):
    appid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    release_date = models.DateField()
    english = models.BooleanField()
    developer = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    required_age = models.IntegerField()
    achievements = models.IntegerField()
    positive_ratings = models.IntegerField()
    negative_ratings = models.IntegerField()
    median_playtime = models.IntegerField()
    average_playtime = models.IntegerField()
    owners = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField()
    short_description = models.TextField()
    steam_image = models.URLField(max_length=255)
    tiny_image = models.URLField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.developer}) - {self.average_playtime} hours average playtime"

    class Meta:
        db_table = 'games'
        managed = False

# game_categories model
class GameCategories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

    class Meta:
        ordering = ['category_name']
        db_table = 'game_categories'
        managed = False

# game_categories_link model
class GameCategoriesLink(models.Model):
    id = models.AutoField(primary_key=True)
    app = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        related_name='game_category_links',
        to_field='appid'
    )
    category = models.ForeignKey(
        GameCategories,
        on_delete=models.CASCADE,
        related_name='category_links',
        to_field='category_id'
    )

    def __str__(self):
        return f"{self.app.name} - {self.category.category_name}"

    class Meta:
        ordering = ['category__category_name']
        db_table = 'game_categories_link'
        managed = False


class GameGenres(models.Model):
    genre_id = models.AutoField(primary_key=True)
    genre_name = models.CharField(max_length=255)

    def __str__(self):
        return self.genre_name

    class Meta:
        ordering = ['genre_name']
        db_table = 'game_genres'
        managed = False

class GameGenresLink(models.Model):
    id = models.AutoField(primary_key=True)
    app = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        related_name='game_genre_links',
        to_field='appid'
    )
    genre = models.ForeignKey(
        GameGenres,
        on_delete=models.CASCADE,
        related_name='genre_links',
        to_field='genre_id'
    )

    def __str__(self):
        return f"{self.app.name} - {self.genre.genre_name}"

    class Meta:
        ordering = ['genre__genre_name']
        db_table = 'game_genres_link'
        managed = False

class GamePlatforms(models.Model):
    platform_id = models.AutoField(primary_key=True)
    platform_name = models.CharField(max_length=255)

    def __str__(self):
        return self.platform_name

    class Meta:
        ordering = ['platform_name']
        db_table = 'game_platforms'
        managed = False

class GamePlatformsLinks(models.Model):
    id = models.AutoField(primary_key=True)
    app = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        related_name='game_platform_links',
        to_field='appid'
    )
    platform = models.ForeignKey(
        GamePlatforms,
        on_delete=models.CASCADE,
        related_name='platform_links',
        to_field='platform_id'
    )

    def __str__(self):
        return f"{self.app.name} - {self.platform.platform_name}"

    class Meta:
        ordering = ['platform__platform_name']
        db_table = 'game_platforms_link'
        managed = False

class GameSteamspyTags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=255)

    def __str__(self):
        return self.tag_name

    class Meta:
        ordering = ['tag_name']
        db_table = 'game_steamspy_tags'
        managed = False


class GameSteamspyTagsLink(models.Model):
    id = models.AutoField(primary_key=True)
    app = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        related_name='game_tag_links',
        to_field='appid'
    )
    tag = models.ForeignKey(
        GameSteamspyTags,
        on_delete=models.CASCADE,
        related_name='tag_links',
        to_field='tag_id'
    )

    def __str__(self):
        return f"{self.app.name} - {self.tag.tag_name}"

    class Meta:
        ordering = ['tag__tag_name']
        db_table = 'game_steamspy_tags_link'
        managed = False

class UserGames(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        'AuthManager.CustomUser',
        on_delete=models.CASCADE,
        related_name='user_games',
        to_field='id'
    )
    app = models.ForeignKey(
        Games,
        on_delete=models.CASCADE,
        related_name='user_games',
        to_field='appid'
    )
    last_played = models.DateField()
    hours_played = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.app.name}"

    class Meta:
        ordering = ['user', 'app']
        db_table = 'user_games'
        managed = False