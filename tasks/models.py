from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_completed= models.DateTimeField(null=True)
    is_important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)#on delete para que si se elimina el usuario, se elimina la tarea tambien

    def __str__(self):
        return self.title + ' created by ' + self.user.username
