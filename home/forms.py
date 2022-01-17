from email.policy import default
from django import forms
from django.forms import ModelForm
from .models import DefaultActivites,goals, activitylog
from .main import myuser,myuser1
from datetime import date as dt

usednames=[]
class defaultactform(ModelForm):
    usednames=[]
    class Meta:
        model = DefaultActivites
        fields = ['name']                    
    def clean_name(self):
    
        result=DefaultActivites.objects.filter(user=myuser[-1])
        for instance in result:
            if instance.name == self.cleaned_data.get('name'):                
                raise forms.ValidationError('This activity has already been added')
        if self.cleaned_data.get('name') in usednames:
            raise forms.ValidationError('This activity has already been added')
        
        usednames.append(self.cleaned_data.get('name'))        

        return self.cleaned_data.get('name')             
            
class goalform(ModelForm):
    class Meta:
        model = goals
        fields = ['name']
class logactform(ModelForm):
    duration=forms.DecimalField(max_digits=4,decimal_places=1,min_value=0,initial=0)
    
    class Meta:
        model=activitylog
        fields=['activity','duration']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice=((None,'None'),)+tuple((act.name, act.name) for act in DefaultActivites.objects.filter(user=myuser1[-1]))
        self.fields['activity'] = forms.ChoiceField( choices= choice)
    def clean_activity(self):
        
        
        for instance in activitylog.objects.filter(user=myuser1[-1]) :
            if instance.activity == self.cleaned_data.get('activity') and instance.date== dt.today():
                
                raise forms.ValidationError('You have already logged activity')
       
        return self.cleaned_data.get('activity')  
