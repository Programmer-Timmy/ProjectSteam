import json

from django.db import models

# new games model
class Games(models.Model):
    appid = models.IntegerField(primary_key=True)
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
        return json.dumps({
            'appid': self.appid,
            'name': self.name,
            'release_date': self.release_date.strftime('%Y-%m-%d'),
            'english': self.english,
            'developer': self.developer,
            'publisher': self.publisher,
            'required_age': self.required_age,
            'achievements': self.achievements,
            'positive_ratings': self.positive_ratings,
            'negative_ratings': self.negative_ratings,
            'median_playtime': self.median_playtime,
            'average_playtime': self.average_playtime,
            'owners': self.owners,
            'price': str(self.price),
        })

    class Meta:
        db_table = 'games'
        managed = False
