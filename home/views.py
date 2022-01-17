from tempfile import template
from winreg import QueryInfoKey
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import defaultactform,goalform,logactform
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
from . main import myuser,myuser1




@login_required(login_url='/')
def registeractivities(request):
    

    ActFormset = formset_factory(defaultactform,extra=10)
    formset= ActFormset()
    if request.method == 'POST':

            myuser.append(request.user)
            formset = ActFormset(request.POST,request.FILES)
            if formset.is_valid():
                for form in formset:
                    
                    
                    if form.cleaned_data:
                        
                                activity=form.save(commit=False)
                                activity.user = request.user                            
                                        
                                       

                                
                                
                                activity.save()
                                                       
                    
                return redirect('homepage')
       
            
   
    return render(request, 'home/registeractivities.html',{'formset':formset})

@login_required(login_url='/')
def registergoals(request):
    GoalFormset = formset_factory(goalform,extra=10)
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
             
      
    return render(request, 'home/registergoals.html',{'formset':formset})

@login_required(login_url='/')
def logactivities(request):
    myuser1.append(request.user)
    count=0
    for i in list(DefaultActivites.objects.filter(user=request.user)):
        count=count+1
    if count==0:
        return render(request,'home/registeractivities.html',{'error':'No default activities added '})
    

    LogFormset = formset_factory(logactform,extra=count)
    formset= LogFormset()
    if request.method == 'POST':

            
            formset = LogFormset(request.POST,request.FILES)
            if formset.is_valid():
                for form in formset:
                    
                    
                    if form.cleaned_data:
                        
                                activity=form.save(commit=False)
                                activity.user = request.user
                                
                                        
                                       

                                
                                
                                
                                activity.save()
                           
                    
                return redirect('homepage')
       
            
      
    return render(request, 'home/registeractivities.html',{'formset':formset})







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

class GoalDetailView(DetailView):
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
        return reverse('viewgoal')

class GoalDeleteView(DeleteView):
    def get_queryset(self):
        return goals.objects.filter(user=self.request.user)
    def get_success_url(self):
        return reverse('viewgoal')


