from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import CustomUser


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditUserForm(forms.Form):
    full_name = forms.CharField(label='Повне ім\'я')
    email = forms.EmailField(label='Поштовий адрес')
    speciality = forms.CharField(label='Спеціальність')

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'field-value'
