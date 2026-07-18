from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path('members/', views.members, name='members'),
    path('admins/', views.admins, name='admins'),
]