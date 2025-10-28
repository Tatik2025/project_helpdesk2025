from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterUserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth import get_user_model


def ListUsers(request):

    class_user = get_user_model()
    users = class_user.objects.filter(is_superuser = False)

    return render(request,"ListUsers.html",{'users':users})

def UserProfile(request):

    if request.method == 'POST':

        form = UserProfileForm(request.POST)

        if not request.POST.get('user_id'):

          if form.is_valid():
                username = form.cleaned_data['username']
                class_user = get_user_model()
                user = class_user.objects.get(username=username)
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

                users = class_user.objects.filter(is_superuser=False)

                return render(request, "ListUsers.html", {'form': form, 'users': users})

          else:
            messages.error(request, "Данные пользователя некорректные!")
        else:

            id = request.POST.get('user_id')
            class_user = get_user_model()
            user = class_user.objects.get(id=id)

            if not user is None:
                initial_data = {
                    'username': user.username,
                    'email': user.email,
                    'first_name':user.first_name,
                    'last_name': user.last_name,
                    'department': user.department,
                    'access_level': user.access_level,
                    }
                form = UserProfileForm(initial=initial_data)
            else:
                messages.error(request, "Пользователь удален!")

                users = class_user.objects.filter(is_superuser=False)

                return render(request, "ListUsers.html", {'form': form, 'users': users})

    else:
        form = UserProfileForm()

    return render(request, 'UserProfile.html', {'form': form})

#LoginView
def LoginView(request):
    if request.method =='POST':
        form=LoginForm(data=request.POST)

        if form.is_valid():
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user=authenticate(request,username=username,password=password)
            if user is not None:
                login(request,user)
                messages.success(request, "Вы успешно вошли!")
                return redirect('app_tasks:index')
            else:
                messages.error(request,"Вход не выполнен!")

        else:
            messages.error(request, "Не удалось авторизоваться!")

    else:
        form=LoginForm()

    return render(request, 'login.html',{'form':form})

#LogoutView
def LogoutView(request):
    logout(request)
    messages.success(request, "Выход осуществлен!")
    return redirect('app_tasks:index')


def RegisterView(request):
    if request.method == 'POST':
        Register_form = RegisterUserForm(request.POST)
        if Register_form.is_valid():
            user = Register_form.save(commit=False)
            user.set_password(Register_form.cleaned_data['password1'])
            user.save()
            messages.success(request, "Вы успешно зарегистрировались!")
            return redirect('app_users:login')
        else:
            messages.error(request, "Данные для регистрации некорректные!")
            return render(request, 'register.html', {'form': Register_form})
    else:
        Register_form = RegisterUserForm()
        return render(request, 'register.html', {'form': Register_form})



