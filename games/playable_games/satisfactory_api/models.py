from django.db import models

class SatisfactoryApi(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=7777)
    password_hash = models.TextField(null=True)
    user = models.ForeignKey(
        'AuthManager.CustomUser',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'satisfactory_api'
        managed = False

