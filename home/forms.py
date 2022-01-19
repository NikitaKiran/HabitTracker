from email.policy import default
from django import forms
from django.forms import ModelForm
from .models import DefaultActivites,goals, activitylog
from .main import myuser,myuser1,myuser2
from datetime import date as dt


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
    duration=forms.DecimalField(max_digits=4,decimal_places=1,min_value=0,initial=0)
    
    class Meta:
        model=activitylog
        fields=['activity','duration']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice=((None,'None'),)+tuple((act.name, act.name) for act in DefaultActivites.objects.filter(user=myuser1[-1]))
        self.fields['activity'] = forms.ChoiceField( choices= choice)
    
class DeleteActForm(forms.Form):
    name=forms.CharField()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choice=((act.name, act.name) for act in DefaultActivites.objects.filter(user=myuser2[-1]))
        self.fields['name'] = forms.ChoiceField( choices= choice,label='Name of activity you want to delete')

