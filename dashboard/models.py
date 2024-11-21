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
        db_table = 'game_categories'
        managed = False

# game_categories_link model
class GameCategoriesLink(models.Model):
    id = models.AutoField(primary_key=True)
    app = models.ForeignKey(Games, on_delete=models.CASCADE, related_name='games', to_field='appid')
    category = models.ForeignKey(GameCategories, on_delete=models.CASCADE, related_name='game_categories', to_field='category_id')

    def __str__(self):
        return f"{self.app.name} - {self.category.category_name}"

    class Meta:
        db_table = 'game_categories_link'
        managed = False
