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
    user = models.ForeignKey('AuthManager.CustomUser', on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey('AuthManager.CustomUser', on_delete=models.CASCADE, related_name='friend')
    status = models.CharField(max_length=255, default='pending')

    def __str__(self):
        return f'{self.user.username} - {self.friend.username}'

    class Meta:
        unique_together = ('user', 'friend')
        verbose_name_plural = 'Friends'
        db_table = 'friends'
        managed = False