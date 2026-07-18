from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("members/", views.members, name="members"),

    path("admins/", views.admins, name="admins"),

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),
    path('profile-update/', views.profile_update, name='profile_update'),

   
]