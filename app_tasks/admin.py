from django.contrib import admin
from . models import Priority, Type_task, Status, Department, Task, User
from django.contrib.auth.admin import UserAdmin

admin.site.register(Priority)
admin.site.register(Type_task)
admin.site.register(Status)
admin.site.register(Department)
admin.site.register(Task)
admin.site.register(User, UserAdmin)
