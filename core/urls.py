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
    path("add-user", views.add_user, name="add_user"),
    path("search-user/<str:ktu_id>", views.search_user),
    path("delete-user/<str:user_id>", views.delete_user),
    path("update-user/<str:user_id>",views.update_user,name="update_user"),
    path("student_manage/", views.student_manage, name="student_manage"),
    path("alumni-approval/",views.alumni_approval,name="alumni_approval"),
    path("user-login/", views.user_login, name="user_login"),
    path("set-password/", views.set_password, name="set_password"),
    path("password-login/", views.password_login, name="password_login"),
    path("dashboard/", views.user_dashboard, name="user_dashboard"),
    path("user-profile-update/", views.user_profile_update, name="user_profile_update"),
    path("change-password/", views.change_password, name="change_password"),
    path("logout/", views.user_logout, name="user_logout"),
    path('placement_management/', views.placement_management, name='placement_management'),
    path('placement-opportunities/', views.placement_opportunities, name='placement_opportunities'),
    path('placement-achievements/', views.placement_achievements, name='placement_achievements'),
    path("placement-updates/",views.placement_updates,name="placement_updates"),
    path("manage_placement/",views.manage_placement,name="manage_placement"),
    path("dis_placement/",views.dis_placement,name="dis_placement"),
    path(
        "student-manage/",
        views.student_manage,
        name="student_manage"
    ),
    path(
        "alumni-approval/",
        views.alumni_approval,
        name="alumni_approval"
    ),
    path("alumni_status/", views.alumni_status, name="alumni_status"),
    path("events/", views.events, name="events"),

]