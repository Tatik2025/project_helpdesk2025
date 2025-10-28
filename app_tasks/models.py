from django.db import models
from django.conf import settings
from django.contrib.auth.models import User, AbstractUser


class Priority(models.Model):
    name = models.CharField(max_length=30)
    deadline = models.IntegerField(blank=False, null=False, default=0)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Status(models.Model):
    name = models.CharField(max_length=30)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(AbstractUser):

    access_level = models.IntegerField(blank=False, default=0)

    department = models.ForeignKey(
        "Department",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )


class Type_task(models.Model):
    name = models.CharField(max_length=100)
    department_id = models.ForeignKey(
        "Department",
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name

class Task(models.Model):
    theme = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000, null=True)
    created_at = models.DateTimeField(null=True)
    completion_Date_actual = models.DateTimeField(null=True)
    completion_Date_plan = models.DateTimeField(null=True)
    date_of_Adoption = models.DateTimeField(null=True)
    priority_id = models.ForeignKey(
        'Priority',
            on_delete=models.PROTECT,
            null=True,
            blank=True,
            default = 1
    )

    status_id = models.ForeignKey(
        'Status',
            on_delete=models.PROTECT,
            null=True,
            blank=True,
            default=3
    )
    department_id = models.ForeignKey(
            Department,
            on_delete=models.PROTECT,
            null=True,
            blank=True
    )
    type_task_id = models.ForeignKey(
            Type_task,
            on_delete=models.PROTECT,
            null=True,
            blank=True,
    )

    user_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="executor"
    )
    author_id = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="creator"
    )
    def __str__(self):
        return self.theme