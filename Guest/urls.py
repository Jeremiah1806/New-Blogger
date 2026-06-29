from django.urls import path
from . import views

urlpatterns = [
    path('UserRegistration/', views.userregistration, name = "userregistration"),
    path('Login/', views.login, name = "login"),
    path('delete_user/<int:id>/', views.delete_user, name="delete_user"),
]