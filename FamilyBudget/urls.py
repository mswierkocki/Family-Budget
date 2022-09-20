from django.contrib import admin
from django.contrib.auth import views
from django.conf.urls import include
from django.urls import path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path("", include("budget_app.urls")),
]
