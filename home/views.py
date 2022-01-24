from tempfile import template
from datetime import date  as dt
from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import defaultactform,goalform,logactform,DeleteActForm,DateForm,SelectActForm,GetMonthForm,GetWeekForm
from django.forms import formset_factory
from .models import goals,DefaultActivites ,activitylog
from django.views.generic import ListView,UpdateView,DeleteView
from django.contrib.auth.decorators import login_required
from .main import myuser
from .get_data import timewise_day,timewise_month,timewise_week,activity_weeks,activity_months,activity_days
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

errormessage='No default activities added. Please add activities to your activity list to be able to log your activity and view trends'


@login_required(login_url='/')
def registeractivities(request): 
    myuser.clear()
    myuser.append(request.user)
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
            messages.success(request,f'Goal(s) Added!')          
            return redirect('homepage')      
    return render(request, 'home/register_act_goal.html',{'formset':formset,'prompt':'Enter any goal you want to track','heading':'Add Goals'})

@login_required(login_url='/')
def logactivities(request):
    myuser.clear()
    myuser.append(request.user)
    count=0
    for i in list(DefaultActivites.objects.filter(user=request.user)):
        count=count+1
    if count==0:
        return render(request,'home/register_act_goal.html',{'error':errormessage})    

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
                messages.success(request,f'Activity logged successfully !')                
                return redirect('homepage')      
    return render(request, 'home/register_act_goal.html',{'formset':formset,'prompt':'Log your activity for the day. If you enter a new duration for an already logged activity, the latest value you enter will be considered.','heading':'Log Actvities'})



@login_required(login_url='/')
def delete_act(request):
    myuser.clear()
    myuser.append(request.user)

    if request.method == 'POST':
        form= DeleteActForm(request.POST)
        if form.is_valid():
            act=DefaultActivites.objects.filter(user=request.user,name=form.cleaned_data.get('name'))   
            act.delete()         
            return redirect('registeractivity')
    else:
        form= DeleteActForm()    
    return render(request, 'home/delete.html',{'form':form})
    




colours=['rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)','rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)',
            'rgba(255, 159, 64, 0.2)']

@login_required(login_url='/')
def home(request):
    labels,values= timewise_week(request.user,0)
    return render(request, 'home/home.html',{'labels':labels,'values':values,'colours':colours,'Goals':list(goals.objects.filter(user=request.user ,done=False))})



class GoalListView(LoginRequiredMixin,ListView):  
    login_url = '/'
    
    context_object_name='Goals'
    ordering=['done']
    def get_queryset(self):
        return goals.objects.filter(user=self.request.user)


    
class GoalUpdateView( LoginRequiredMixin,UpdateView):
    
    fields = ['done']
    def get_queryset(self):
        return goals.objects.filter(user=self.request.user)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('goal-list')

class GoalDeleteView(LoginRequiredMixin,DeleteView):
    def get_queryset(self):
        return goals.objects.filter(user=self.request.user)
    def get_success_url(self):
        return reverse('goal-list')



@login_required(login_url='/')
def timewise_trends_daily(request):
    count=0
    
    for i in list(DefaultActivites.objects.filter(user=request.user)):
        count=count+1
    if count==0:
        return render(request,'home/time_trends.html',{'error1':errormessage})
    date1=dt.today()
    if request.method == 'POST':        
        form= DateForm(request.POST)
        if form.is_valid():
            date1=form.cleaned_data.get('date')
    else:
        form= DateForm() 
    label1,value1=timewise_day(request.user,date1)
    
    
    
    return render(request, 'home/time_trends.html',{'form':form,'heading':'Daily ','labels':label1,'values':value1,'colours':colours})
@login_required(login_url='/')
def timewise_trends_weekly(request):
    count=0
    
    for i in list(DefaultActivites.objects.filter(user=request.user)):
        count=count+1
    if count==0:
        return render(request,'home/time_trends.html',{'error1':errormessage})
    week=0
    if request.method == 'POST':        
        form= GetWeekForm(request.POST)
        if form.is_valid():
            week=int(form.cleaned_data.get('week'))
    else:
        form= GetWeekForm() 
    label1,value1= timewise_week(request.user,week)
    
    
    
    return render(request, 'home/time_trends.html',{'form':form,'heading':'Weekly','labels':label1,'values':value1,'colours':colours})
@login_required(login_url='/')
def timewise_trends_monthly(request):
    count=0
    
    for i in list(DefaultActivites.objects.filter(user=request.user)):
        count=count+1
    if count==0:
        return render(request,'home/time_trends.html',{'error1':errormessage})
    month=dt.today().month
    if request.method == 'POST':        
        form= GetMonthForm(request.POST)
        if form.is_valid():
            month=int(form.cleaned_data.get('month'))
    else:
        form= GetMonthForm() 
    label1,value1=timewise_month(request.user,month)
    
    
    
    
    return render(request, 'home/time_trends.html',{'form':form,'heading':'Monthly','labels':label1,'values':value1,'colours':colours})
@login_required(login_url='/')
def act_trends_daily(request):
    count=0
    
    for i in list(DefaultActivites.objects.filter(user=request.user)):
        count=count+1
    if count==0:
        return render(request,'home/time_trends.html',{'error1':errormessage}) 
    myuser.clear()
    myuser.append(request.user)
    activity=DefaultActivites.objects.filter(user=request.user)[0].name
    if request.method == 'POST':        
        form= SelectActForm(request.POST)
        if form.is_valid():
            activity=form.cleaned_data.get('name')
    else:
        form= SelectActForm() 
    label1,value1=activity_days(request.user,activity)
    
   
    
    return render(request, 'home/time_trends.html',{'form':form,'heading':'Daily','labels':label1,'values':value1,'colours':colours})
@login_required(login_url='/')
def act_trends_weekly(request):
    count=0
    
    for i in list(DefaultActivites.objects.filter(user=request.user)):
        count=count+1
    if count==0:
        return render(request,'home/time_trends.html',{'error1':errormessage}) 
    myuser.clear()
    myuser.append(request.user)
    activity=DefaultActivites.objects.filter(user=request.user)[0].name
    if request.method == 'POST':        
        form= SelectActForm(request.POST)
        if form.is_valid():
            activity=form.cleaned_data.get('name')
    else:
        form= SelectActForm() 
    label1,value1=activity_weeks(request.user,activity)
    
    return render(request, 'home/time_trends.html',{'form':form,'heading':'Weekly','labels':label1,'values':value1,'colours':colours})

@login_required(login_url='/')
def act_trends_monthly(request):
    
    count=0
    for i in list(DefaultActivites.objects.filter(user=request.user)):
        count=count+1
    if count==0:
        return render(request,'home/time_trends.html',{'error1':errormessage}) 
    myuser.clear()
    myuser.append(request.user)
    activity=DefaultActivites.objects.filter(user=request.user)[0].name
    if request.method == 'POST':        
        form= SelectActForm(request.POST)
        if form.is_valid():
            activity=form.cleaned_data.get('name')
    else:
        form= SelectActForm() 
    label1,value1=activity_months(request.user,activity)
    
    
    
    return render(request, 'home/time_trends.html',{'form':form,'heading':'Monthly','labels':label1,'values':value1,'colours':colours})