from django.db import models
from django.contrib.auth.models import User

class UserInterests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.CharField(max_length=20)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=2000)
    img = models.ImageField(upload_to ='uploads/')
    time = models.DateTimeField()
    location = models.CharField(max_length=50)
    topic = models.CharField(max_length=20,blank=True)

class ProfilePic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to ='profilepics/')
    time = models.DateTimeField()

class Like(models.Model):
    post= models.ForeignKey(Post,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    time = models.DateTimeField()

class Friend(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE,related_name='sender')
    user2 = models.IntegerField()
    accepted = models.BooleanField()
    time = models.DateTimeField()



