from django import forms
from app_tasks.models import Priority, Task, Department, Status,Type_task
from django.forms import ModelForm
from django.contrib.auth import get_user_model
from datetime import datetime


class TaskDetailForm(forms.Form):


    def __init__(self, *args, **kwargs):
        #user = kwargs.pop('user', None)
        super(TaskDetailForm, self).__init__(*args, **kwargs)

        # if user.access_level ==0:
        #     self.fields['description'].initial = 'Ghbdtn0'
        # if user.access_level ==1:
        #     self.fields['description'].initial = 'Ghbdtn1'
        # if user.access_level ==2:
        #     self.fields['description'].initial = 'Ghbdtn2'
        #self.fields['author_id'].widget.attrs['readonly'] = True


    class_user = get_user_model()

    task_id = forms.IntegerField(label="Заявка №", widget=forms.TextInput(
        attrs={'class': 'form-control', 'readonly': 'readonly','style': 'width: 100px; text-align: center;'}))

    type_task_id = forms.ModelChoiceField(queryset=Type_task.objects, label="Тип Заявки",
                                          empty_label="Не выбран тип заявки",
                                          widget=forms.Select(attrs={'class': 'form-control'}))

    theme = forms.CharField(max_length=100, label="Тема", widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Введите тему заявки'}))

    priority_id = forms.ModelChoiceField(queryset=Priority.objects, label="Важность",
                                         widget=forms.Select(attrs={'class': 'form-control'}))

    status_id = forms.ModelChoiceField(queryset=Status.objects, label="Статус",
                                       widget=forms.Select(attrs={'class': 'form-control'}))

    department_id = forms.ModelChoiceField(queryset=Department.objects, label="Подразделение",
                                           widget=forms.Select(attrs={'class': 'form-control'}))

    user_id = forms.ModelChoiceField(queryset=class_user.objects, label="Исполнитель",
                                     widget=forms.Select(attrs={'class': 'form-control'}))

    description = forms.CharField(max_length=1000, label="Описание", widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Введите описание заявки'}))

    completion_Date_plan = forms.DateTimeField(label="Дата выполнения (план)", widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local', 'class': 'form-control datetimepicker-input'}))

    completion_Date_actual = forms.DateTimeField(label="Дата выполнения (факт)", widget=forms.DateTimeInput(
        attrs={'class': 'form-control datetimepicker-input','disabled': 'disabled'}))

    Date_of_Adoption = forms.DateTimeField(label="Дата принятия в работу", widget=forms.DateTimeInput(
        attrs={'type': 'datetime-local', 'class': 'form-control datetimepicker-input', 'disabled': 'disabled'}))

    created_at = forms.DateTimeField(label="Дата создания", widget=forms.DateTimeInput(
        attrs={'class': 'form-control datetimepicker-input', 'disabled': 'disabled'}))

    author_id = forms.ModelChoiceField(queryset=class_user.objects, label="Автор",
                                       widget=forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}))

    class Meta:
        fields=('type_task_id','theme','priority_id','status_id','description','department_id','user_id','author_id','created_at','completion_Date_actual','completion_Date_plan','Date_of_Adoption',)
