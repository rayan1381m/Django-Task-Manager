from django import forms
from .models import Task

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description']
        
class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status']
        
class searchForm(forms.Form):
    search = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'search...'}), required=False)      