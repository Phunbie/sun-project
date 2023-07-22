from django.db import models
from PIL import Image as Im 
from django.contrib.auth.models import User


class Team(models.Model):
    name = models.CharField(max_length=255)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null = True)
    country = models.CharField(max_length=100)

class Task(models.Model):
    task = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    region = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    selected = models.BooleanField(default=False)
    approve = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    user_id = models.IntegerField(default=0)
    team_id = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
   

class Visit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    mission = models.ForeignKey(Task, on_delete=models.CASCADE)
    goal = models.IntegerField()
    achievement = models.IntegerField()
    notes = models.TextField()
    picture = models.ImageField(upload_to='pics')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    

class UserTeam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    month = models.DateField()
    goal = models.IntegerField()
    achievement = models.IntegerField()
   

class Audit(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    date = models.DateField()
    findings = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
