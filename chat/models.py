from django.db import models
#from django.db import IntegrityError

class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)
    ans = models.CharField(max_length=200,default="abss")


    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Problem(models.Model):


    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    prob_ques = models.CharField(max_length=1000, null=True)
    answer = models.CharField(max_length=1000)
   

    def __str__(self):
        
        return self.prob_ques