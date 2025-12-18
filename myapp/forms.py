from django import forms
from .models import Application
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import  ChatMessage
from .models import Employee,Works
from django.forms import ModelForm,TextInput,Textarea



class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application  # Критически важная строка!
        fields = ['name', 'email', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Пожалуйста, введите корректный email адрес")
        return email


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Введите ваше сообщение...',
                'class': 'form-control'
            }),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['name', 'position', 'photo', 'bio', 'is_published', 'order']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }
class WorksForm(forms.ModelForm):
    class Meta:
        model = Works
        fields = ['name', 'photo', 'bio', 'is_published', 'order']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }