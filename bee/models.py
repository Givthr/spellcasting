from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=50)

    def __str__(self):
        return self.nickname

class PlayerScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="scores")
    score = models.IntegerField()
    difficulty = models.CharField(max_length=20, default="easy")
    date_achieved = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        profile_name = getattr(self.user.playerprofile, 'nickname', self.user.username)
        return f"{profile_name} - {self.score} ({self.difficulty})"