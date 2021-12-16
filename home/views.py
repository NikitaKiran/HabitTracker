from django.shortcuts import render
# Create your views here.
import mysql.connector

labels=['Exercise','Dance','Study','Sleep','Math','Cook','Read','Code']
values=[1.5,.5,2,9,1,6,7,1]
colourset=['rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)']
colours=[]
for i in range(len(labels)):
    colours.append(colourset[i%6])

def home(request):
    return render(request, 'home/home.html',{'labels':labels,'values':values,'colours':colours})


