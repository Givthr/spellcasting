from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return self.nickname

class PlayerScore(models.Model):
    name = models.CharField(max_length=50, default="Anonymous")
    score = models.IntegerField()
    difficulty = models.CharField(max_length=20, default="easy")
    date_achieved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.score} ({self.difficulty})"