from django.urls import path, include
from .import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "app_users"

urlpatterns = [

    path('login/', views.LoginView, name="login"),
    path('logout/', views.LogoutView, name="logout"),
    path('register/', views.RegisterView, name="register"),
    path('listusers/', views.ListUsers, name="listusers"),
    path('userprofile/', views.UserProfile, name="userprofile"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)