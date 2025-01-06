from django.db import models

# Create your models here.
class Friend(models.Model):
    """
    Friend model

    This model is used to store the relationship between two users.

    Attributes:
    - user: The user who sent the friend request.
    - friend: The user who received the friend request.
    - status: The status of the friend request (pending, accepted
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('AuthManager.CustomUser', on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey('AuthManager.CustomUser', on_delete=models.CASCADE, related_name='friend', null=True, blank=True)
    status = models.CharField(max_length=255, default='friends')
    steam_id = models.CharField(max_length=255, null=True) # this is for when the friend does not have an account on the site
    friend_name = models.CharField(max_length=255, null=True)
    avatar_url = models.CharField(max_length=255, null=True)

    def __str__(self):
        if self.steam_id:
            return f'{self.user.username} - {self.steam_id}'

        return f'{self.user.username} - {self.friend.username}'

    def add_friend(self, user, friend):
        """
        Add a friend to the database.

        Parameters:
        - user: The user who sent the friend request.
        - friend: The user who received the friend request.
        """
        self.user = user
        self.friend = friend
        self.save()

    def add_steam_id(self, user, steam_id):
        """
        Add a steam id to the database.

        Parameters:
        - steam_id: The steam id of the user who received the friend request.
        """
        self.user = user
        self.steam_id = steam_id
        self.save()

    class Meta:
        unique_together = ('user', 'friend')
        verbose_name_plural = 'Friends'
        db_table = 'friends'
        managed = False