from django.db import models
#from django.db import IntegrityError

#from django.contrib.auth.models import AbstractUser

from django.db import models
from django.contrib.auth.models import User

from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):    
    def is_open_for_signup(self, request):
        return False


class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255,default="abss")
    ans = models.CharField(max_length=200,default="abss")
    max_players = models.IntegerField(default=0)
    room_status = models.CharField(max_length=100, default="Closed")   #status of room wheteher it is open or closed
    ques_num = models.IntegerField(default=1)

    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Problem(models.Model):

    ques_no = models.IntegerField(default=1)
    prob_ques = models.CharField(max_length=1000, null=True)
    ques_answer = models.CharField(max_length=1000)
   

    def __str__(self):
        
        return self.prob_ques

class Player(models.Model):
    name = models.OneToOneField(User,on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    room = models.CharField(max_length=10000)
    ans_given = models.CharField(max_length=100000)
    ans_status = models.CharField(max_length=100000,default="offline")

    def __str__(self):
        return self.name.username