from django import forms
#from django.forms import ModelForm, TextInput, EmailInput
from .models import Task, Profile, Team, Visit, User
from django.forms import DateField

"""class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = ['selected']
        widgets = {
            'role': forms.RadioSelect(choices=[('Select', 'Select'), ('Unselect', 'Unselect')]),
        }"""

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['selected']


class ComleteTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['completed']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'region', 'area', 'country','team']
        widgets = {
            'role': forms.RadioSelect(choices=[('Manager', 'Manager'), ('Staff', 'Staff')]),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['team'] = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label=None)#Team.objects.all()Team.objects.filter(user=user)

    
"""
class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Visit
        fields = ['user','date', 'mission', 'goal', 'achievement', 'notes', 'picture']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['mission'].queryset = Task.objects.filter(user=user)
        #self.fields['mission'].queryset = Task.objects.all()
"""
class ImageUploadForm(forms.ModelForm):
    date = DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Visit
        fields = ['date', 'mission', 'goal', 'achievement', 'notes', 'picture']
