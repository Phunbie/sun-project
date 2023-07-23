from django import forms
from django.forms import ModelForm, TextInput, EmailInput
from .models import Task, Profile, Team

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

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'region', 'area', 'country']
        widgets = {
            'role': forms.RadioSelect(choices=[('Manager', 'Manager'), ('Staff', 'Staff')]),
        }


    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['team'] = forms.ModelChoiceField(queryset=Team.objects.all(), empty_label=None)#Team.objects.all()Team.objects.filter(user=user)

