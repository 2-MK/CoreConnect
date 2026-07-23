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
    path('alumni-directory/', views.alumni_directory, name='alumni_directory'),
    path("get-users", views.get_users),
    path("add-user", views.add_user),
    path("update-user", views.update_user, name="update_user"),
    path("delete-user", views.delete_user, name="delete_user"),
    path("user-login/", views.user_login, name="user_login"),
path("set-password/", views.set_password, name="set_password"),
path("password-login/", views.password_login, name="password_login"),
path("dashboard/", views.user_dashboard, name="user_dashboard"),
path("user-profile-update/", views.user_profile_update, name="user_profile_update"),
path("change-password/", views.change_password, name="change_password"),
path("logout/", views.user_logout, name="user_logout"),
]