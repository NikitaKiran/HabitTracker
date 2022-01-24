from django import forms
from django.forms import ModelForm
from .models import DefaultActivites,goals, activitylog
from .main import myuser
from datetime import date as dt,timedelta as td


class defaultactform(ModelForm):    
    class Meta:
        model = DefaultActivites
        fields = ['name']                    
    def clean_name(self):    
        result=DefaultActivites.objects.filter(user=myuser[-1])
        for instance in result:
            if instance.name == self.cleaned_data.get('name'):                
                raise forms.ValidationError('This activity has already been added')
        return self.cleaned_data.get('name')             
            
class goalform(ModelForm):
    class Meta:
        model = goals
        fields = ['name']

class logactform(ModelForm):
    duration=forms.DecimalField(max_digits=4,decimal_places=1,min_value=0,initial=0,label='Duration in hours')
    class Meta:
        model=activitylog
        fields=['activity','duration']        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice=((None,'None'),)+tuple((act.name, act.name) for act in DefaultActivites.objects.filter(user=myuser[-1]))
        self.fields['activity'] = forms.ChoiceField( choices= choice)
        
class DeleteActForm(forms.Form):
    name=forms.CharField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice=((act.name, act.name) for act in DefaultActivites.objects.filter(user=myuser[-1]))
        self.fields['name'] = forms.ChoiceField( choices= choice,label='Name of activity you want to delete')
 
class DateForm(forms.Form):    
    date=forms.DateField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice=()
        for i in range(7):
            choice+=((dt.today() - td(days = i),dt.today() - td(days = i)),)       
        self.fields['date'] = forms.ChoiceField( choices= choice,label='Select date:')

class GetMonthForm(forms.Form):
    month=forms.IntegerField(min_value=1,max_value=12)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice=()        
        for i in range(1,13):
            year1=dt.today().year   
            if i>dt.today().month :
                year1=dt.today().year - 1            
            choice+=((i, dt(1900, i, 1).strftime('%B')+' , '+str(year1)),)        
        self.fields['month'] = forms.ChoiceField( choices= choice,label='Select month:',initial=dt.today().month)

class GetWeekForm(forms.Form):
    week=forms.IntegerField(min_value=0,max_value=3)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice=()        
        for i in range(4):                     
            choice+=((i, str(dt.today()-td(days=7*(i+1)-1))+' to '+str(dt.today()-td(days=7*i))),)        
        self.fields['week'] = forms.ChoiceField( choices= choice,label='Select week:')    

class SelectActForm(forms.Form):
    name=forms.CharField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice=((act.name, act.name) for act in DefaultActivites.objects.filter(user=myuser[-1]))
        self.fields['name'] = forms.ChoiceField( choices= choice,label='Select Activity :')


