from django.shortcuts import render, redirect
from .forms import TaskDetailForm
from django.contrib import messages
from app_tasks.models import Type_task, Task,Priority
import datetime
import json


def index(request):
    if request.user.is_authenticated:
        access_level = request.user.access_level
        department = request.user.department
        user_tasks = Task.objects.filter(author_id = request.user.pk)
        tasks_for_user = 2
        tasks_without_executor=3
        all_tasks = 4
        if access_level ==0:
             context = {'user_tasks': user_tasks, 'access_level': access_level}
        elif access_level == 1:
            context = {'user_tasks': user_tasks, 'tasks_for_user': tasks_for_user, 'tasks_without_executor': tasks_without_executor,'access_level': access_level}
        elif access_level == 2:
            context = {'user_tasks':user_tasks,'tasks_for_user':tasks_for_user,'all_tasks':all_tasks, 'access_level':access_level}

        return render(request,"index.html",context)
    else:
        return redirect('app_users:login')


def TaskDetail(request):

    if request.method == 'POST':

        form =  TaskDetailForm(request.POST)

        if not request.POST.get('task_id'):

            if form.is_valid():
                task_id = form.cleaned_data['task_id']
                user = Task.objects.get()
                if not user is None:
                    list_update_fields = []

                    if form.cleaned_data['first_name'] != user.first_name:
                        user.first_name = form.cleaned_data['first_name']
                        list_update_fields.append('first_name')

                    if form.cleaned_data['last_name'] != user.last_name:
                        user.last_name = form.cleaned_data['last_name']
                        list_update_fields.append('last_name')

                    if form.cleaned_data['email'] != user.email:
                        user.email = form.cleaned_data['email']
                        list_update_fields.append('email')

                    if form.cleaned_data['department'] != user.department:
                        user.department = form.cleaned_data['department']
                        list_update_fields.append('department')

                    if form.cleaned_data['access_level'] != user.access_level:
                        user.access_level = form.cleaned_data['access_level']
                        list_update_fields.append('access_level')

                    if list_update_fields:
                        user.save(update_fields=list_update_fields)

                else:
                    messages.error(request, "Пользователь удален!")


                return render(request, "ListUsers.html", {'form': form})

            else:
                messages.error(request, "Данные пользователя некорректные!")
        else:

            task_id = request.POST.get('task_id')
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
        form = TaskDetailForm(initial=initial_data)

    type_task_qs = Type_task.objects.all()
    list_of_dicts_type_task = list(type_task_qs.values())
    priority_qs = Priority.objects.all()
    list_of_dicts_priority = list(priority_qs.values())

    return render(request, 'taskdetail.html', {'form': form,'list_of_dicts_priority':json.dumps(list_of_dicts_priority),'list_of_dicts_type_task':json.dumps(list_of_dicts_type_task)})
