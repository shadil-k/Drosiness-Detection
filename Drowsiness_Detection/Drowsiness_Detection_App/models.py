from django.db import models

# Create your models here.


class Login(models.Model):
    objects = None
    Username = models.CharField(max_length=30)
    Password = models.CharField(max_length=30)
    Type = models.CharField(max_length=10)


class User(models.Model):
    objects = None
    Firstname = models.CharField(max_length=50)
    Lastname = models.CharField(max_length=50)
    Gender = models.CharField(max_length=10)
    Place = models.CharField(max_length=50)
    Post = models.CharField(max_length=50)
    Pin = models.BigIntegerField()
    Email = models.CharField(max_length=100)
    Phone = models.BigIntegerField()
    Vehicle = models.CharField(max_length=50)
    LID = models.ForeignKey(Login, on_delete=models.CASCADE)


class Complaints(models.Model):
    objects = None
    Complaint = models.CharField(max_length=300)
    Date = models.DateField()
    Reply = models.CharField(max_length=300)
    UID = models.ForeignKey(User, on_delete=models.CASCADE)


class Music(models.Model):
    objects = None
    Musics = models.FileField()
    Details = models.CharField(max_length=100)
    Date = models.DateField()
    Emotions = models.CharField(max_length=100)


class Feedback(models.Model):
    objects = None
    Feedbacks = models.CharField(max_length=300)
    Date = models.DateField()
    UID = models.ForeignKey(User, on_delete=models.CASCADE)
