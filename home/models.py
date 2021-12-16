from django.db import models
from django.contrib.auth.models import User
from django.db.models.constraints import CheckConstraint

class Goal(models.Model):
    name=models.CharField(max_length=50)
    startdate = models.DateField()
    enddate = models.DateField()
    category = models.CharField(max_length=20)
    
    user= models.ForeignKey(User,on_delete=models.CASCADE)
