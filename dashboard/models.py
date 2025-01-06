from django.db import models

from games.models import Games

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

class GameSessions(models.Model):
    id = models.AutoField(primary_key=True)
    user_game = models.ForeignKey(
        UserGames,
        on_delete=models.CASCADE,
        related_name='game_sessions',
        to_field='id'
    )
    start_timestamp = models.DateTimeField(null=False, auto_now_add=True)
    end_timestamp = models.DateTimeField(null=True)
    total_time = models.FloatField()
    ongoing = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user_game.user.username} - {self.user_game.app.name} - {self.start_timestamp}"

    class Meta:
        ordering = ['user_game', 'start_timestamp']
        db_table = 'game_sessions'
        managed = False