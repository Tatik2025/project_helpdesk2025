from django.db.transaction import commit
from django.shortcuts import render, redirect
from .forms import TaskDetailForm,TaskCreateForm
from django.contrib import messages
from app_tasks.models import Type_task, Task,Priority
from django.db.models import Q
import datetime
import json


"""
Получаем список заявок
Нулевой уровень доступа: заявки, в которых автор = текущий пользователь
Первый уровень доступа: заявки, в которых автор = текущий пользователь, исполнитель= текущий пользователь
и заявки без исполнителя у которых такой же отдел как у пользователя
Второй уровень доступа: все заявки
Суперпользователь: все заявки
"""
def get_list_tasks(user):

    access_level = user.access_level

    if not  user.is_superuser:
        department_id = user.department_id

    if access_level == 2 or user.is_superuser:
        user_tasks = Task.objects.all()
        context2 = {'user_tasks': user_tasks}

    elif access_level == 0:
        user_tasks = Task.objects.filter(author_id = user.id)
        context2 = {'user_tasks': user_tasks}

    elif access_level == 1:
        user_tasks = Task.objects.filter(
            Q(author_id=user.id)|
            Q(user_id=user.id)|
            (Q(user_id__isnull=True)&
             Q(department_id=department_id))
        )
        context2 = {'user_tasks': user_tasks}

    return context2

#для корректного отображения адреса http://127.0.0.1:8000/
def basepage(request):
    return redirect('app_tasks:index')

#Вывод главной страницы
def index(request):
    if request.user.is_authenticated:

        context = get_list_tasks(request.user)

        return render(request,"index.html",context)

    else:

        return redirect('app_users:login')

#Функция для создания и редактирования заявки
def TaskDetail(request):

    if request.method == 'POST':

        if not request.POST.get('task_id_edit'):

            if request.POST.get('task_id') != '':

                form = TaskDetailForm(request.POST)

                if form.is_valid():
                    task_id = form.cleaned_data['task_id']
                    task = Task.objects.get(id=task_id)
                    if not task is None:
                        list_update_fields = []

                        if form.cleaned_data['type_task_id'] != task.type_task_id:
                            task.type_task_id = form.cleaned_data['type_task_id']
                            list_update_fields.append('first_name')

                        if form.cleaned_data['theme'] != task.theme:
                            task.theme = form.cleaned_data['theme']
                            list_update_fields.append('theme')

                        if form.cleaned_data['priority_id'] != task.priority_id:
                            task.priority_id = form.cleaned_data['priority_id']
                            list_update_fields.append('priority_id')

                        if form.cleaned_data['status_id'] != task.status_id:
                            task.status_id = form.cleaned_data['status_id']
                            list_update_fields.append('status_id')
                        if form.cleaned_data['user_id'] != task.user_id:
                            task.user_id = form.cleaned_data['user_id']
                            list_update_fields.append('user_id')

                        if form.cleaned_data['completion_Date_plan'] != task.completion_Date_plan:
                            task.completion_Date_plan = form.cleaned_data['completion_Date_plan']
                            list_update_fields.append('completion_Date_plan')

                        if list_update_fields:
                            task.save(update_fields=list_update_fields)
                        return redirect('app_tasks:index')
                    else:
                        messages.error(request, "Заявка удалена!")
                else:
                    messages.error(request, "Данные заявки некорректные!")
            else:
                form = TaskCreateForm(request.POST)

                if form.is_valid():
                    task = form.save(commit=False)
                    task.author_id = request.user
                    task.created_at = datetime.datetime.now()
                    task.save()

                    return redirect('app_tasks:index')

                else:
                    messages.error(request, "Данные заявки некорректные!")

        else:

            task_id = request.POST.get('task_id_edit')
            task = Task.objects.get(id=task_id)

            if not task is None:
                initial_data = {
                    'task_id': task.id,
                    'theme': task.theme,
                    "type_task_id": task.type_task_id,
                    "priority_id": task.priority_id,
                    "status_id": task.status_id,
                    "description": task.description,
                    "department_id": task.department_id,
                    "user_id": task.user_id,
                    "author_id": task.author_id,
                    "created_at": task.created_at,
                    "completion_Date_actual": task.completion_Date_actual,
                    "completion_Date_plan": task.completion_Date_plan,
                    "date_of_Adoption": task.date_of_Adoption,
                }
                form = TaskDetailForm(initial=initial_data)
            else:
                messages.error(request, "Возможно заявка удалена!")

                return render(request, "index.html", {'form': form})

    else:
        initial_data = {
            "author_id": request.user,
        }
        form = TaskCreateForm(initial=initial_data)

    type_task_qs = Type_task.objects.all()
    list_of_dicts_type_task = list(type_task_qs.values())
    result_dict_type_task = {d['id']: d for d in list_of_dicts_type_task}

    priority_qs = Priority.objects.all()
    list_of_dicts_priority = list(priority_qs.values())

    return render(request, 'taskdetail.html',
                  {'form': form, 'list_of_dicts_priority': json.dumps(list_of_dicts_priority),
                   'dicts_type_task': json.dumps(result_dict_type_task)})
