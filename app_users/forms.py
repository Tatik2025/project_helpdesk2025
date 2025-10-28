from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from app_tasks.models import Priority, Task, Department, Status,Type_task
from django.forms import ModelForm

from datetime import datetime


#LoginForm
class LoginForm(AuthenticationForm):
    username=forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class UserProfileForm(forms.Form):

    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}))
    email = forms.CharField(label='Эл.почта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    #password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    #password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    department = forms.ModelChoiceField(queryset=Department.objects, label="Подразделение",
                                        widget=forms.Select(attrs={'class': 'form-control'}))
    access_level = forms.IntegerField(label='Уровень доступа',min_value=0, max_value=2, widget=forms.NumberInput())

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'department','access_level',)

    def clean(self):
        email       = self.cleaned_data['email']
        username    = self.cleaned_data['username']
        if get_user_model().objects.filter(email=email).exists() and get_user_model().objects.get(email=email).username != username:
            raise forms.ValidationError("Такой E-mail уже существует!")

#RegisterForm
class RegisterUserForm(UserCreationForm):

    first_name      = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name       = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
    username        = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email           = forms.CharField(label='Эл.почта', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1       = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2       = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    department      = forms.ModelChoiceField(queryset=Department.objects, label="Подразделение",widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model=get_user_model()
        fields=('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'department')

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


