from tempfile import template
from datetime import date  as dt
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import defaultactform,goalform,logactform,DeleteActForm
from django.forms import formset_factory
from .models import goals,DefaultActivites ,activitylog
from django import forms
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.contrib.auth.decorators import login_required
from .main import myuser,myuser1,myuser2





@login_required(login_url='/')
def registeractivities(request): 
    myuser.clear()
    myuser.append(request.user)
    print(myuser2,myuser,myuser1)
    count=0
    for i in list(DefaultActivites.objects.filter(user=request.user)):
        count=count+1  
    count=10-count
    ActFormset = formset_factory(defaultactform,extra=  count)
    formset= ActFormset()
    if request.method == 'POST':
            myuser.append(request.user)
            formset = ActFormset(request.POST,request.FILES)
            
            for form in formset:  
                if form.is_valid():                
                    if form.cleaned_data:
                        activity=form.save(commit=False)
                        activity.user = request.user                    
                        activity.save()                                                      
                    
            return redirect('registeractivity')
    act_list=list(DefaultActivites.objects.filter(user=request.user) )    
    
    return render(request, 'home/register_act_goal.html',{'formset':formset,'prompt':'Enter the activities you want to add to your daily activity list. E.g Excercise,Sleep etc. You can have upto 10 daily activities.','heading':'Daily Activitity List','actlist':act_list,'empty':not bool(count)})

@login_required(login_url='/')
def registergoals(request):
    GoalFormset = formset_factory(goalform,extra=5)
    formset= GoalFormset()
    if request.method == 'POST':
        formset = GoalFormset(request.POST,request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:                    
                    goal=form.save(commit=False)
                    goal.user = request.user
                    if form.is_valid:
                        goal.save()                   
            
            return redirect('homepage')            
      
    return render(request, 'home/register_act_goal.html',{'formset':formset,'prompt':'Enter any goal you want to track','heading':'Add Goals'})

@login_required(login_url='/')
def logactivities(request):
    myuser1.clear()
    myuser1.append(request.user)
    count=0
    for i in list(DefaultActivites.objects.filter(user=request.user)):
        count=count+1
    if count==0:
        return render(request,'home/register_act_goal.html',{'error':'No default activities added '})    

    LogFormset = formset_factory(logactform,extra=count)
    formset= LogFormset()
    if request.method == 'POST':            
            formset = LogFormset(request.POST,request.FILES)
            if formset.is_valid():
                for form in formset:                 
                    if form.cleaned_data: 
                        for instance in activitylog.objects.filter(user=request.user,date= dt.today()) :
                            if instance.activity == form.cleaned_data.get('activity')  :
                                instance.duration=form.cleaned_data.get('duration')
                                instance.save() 
                                break
                        else:                                       
                            activity=form.save(commit=False)
                            activity.user = request.user                            
                            activity.save()                 
                return redirect('homepage')      
    return render(request, 'home/register_act_goal.html',{'formset':formset,'prompt':'Log your activity for the day. If you enter a new duration for an already logged activity, the latest value you enter will be considered.','heading':'Log Actvities'})



@login_required(login_url='/')
def delete_act(request):
    myuser2.clear()
    myuser2.append(request.user)

    if request.method == 'POST':
        form= DeleteActForm(request.POST)
        if form.is_valid():
            act=DefaultActivites.objects.filter(user=request.user,name=form.cleaned_data.get('name'))   
            act.delete()         
            return redirect('registeractivity')
    else:
        form= DeleteActForm()    
    return render(request, 'home/delete.html',{'form':form})
    



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
    return render(request, 'home/home.html',{'labels':labels,'values':values,'colours':colours,'Goals':list(goals.objects.filter(user=request.user ,done=False))})
def time_trends(request):
    return render(request, 'home/time_trends.html',{'labels':labels,'values':values,'colours':colours})
def act_trends(request):
    return render(request, 'home/act_trends.html',{'labels':labels,'values':values,'colours':colours})

class GoalListView(ListView):  
    
    context_object_name='Goals'
    ordering=['done']
    def get_queryset(self):
        return goals.objects.filter(user=self.request.user)


    
class GoalUpdateView( UpdateView):
    
    fields = ['done']
    def get_queryset(self):
        return goals.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('goal-list')

class GoalDeleteView(DeleteView):
    def get_queryset(self):
        return goals.objects.filter(user=self.request.user)
    def get_success_url(self):
        return reverse('goal-list')





