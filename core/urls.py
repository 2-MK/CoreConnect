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
    path('users_details/', views.user_details_view, name='user_details'),
    path("get-users", views.get_users),
    path("add-user", views.add_user),
    path("update-user", views.update_user, name="update_user"),
    path("delete-user", views.delete_user, name="delete_user"),
   
]