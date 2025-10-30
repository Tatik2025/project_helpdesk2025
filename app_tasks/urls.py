from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "app_tasks"

urlpatterns = [
    path('', views.basepage, name="index"),
    path('index/', views.index, name="index"),
    path('taskdetails/', views.TaskDetail, name="taskdetails"),
    path('users', include('app_users.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
