from ast import mod
from django.db import models
from django.contrib.auth.models import User
from django.db.models.constraints import CheckConstraint
import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class DefaultActivites(models.Model):   
    
    name=models.CharField('Activity Name:',max_length=50)
    user= models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    class Meta:
        unique_together=[['name','user']]

class goals(models.Model):
    name=models.CharField('Goal Name:',max_length=50)
    done=models.BooleanField(default=False)
    user= models.ForeignKey(User,on_delete=models.CASCADE)

class activitylog(models.Model):
    activity=models.CharField(max_length=50)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    duration=models.DecimalField(max_digits=4,decimal_places=1,default=0)





