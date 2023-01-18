from django import forms
from .models import Task

class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields=['title','description','is_important']
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control mb-3'}),
            'description': forms.Textarea(attrs={'class':'form-control mb-3', 'placeholder':'Describe the details of your task.'}),
            'is_important': forms.CheckboxInput(attrs={'class':'form-check-input m-auto mb-3'}),
        }

#formulario para enviar a frontend.