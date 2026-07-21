from django.shortcuts import render, redirect
from .supabase_client import supabase
from django.http import JsonResponse
import json


def home(request):
    return render(request, "home/home.html")

def members(request):
    return render(request, "home/members.html")  

def admins(request):

    if request.method == "POST":

        name = request.POST.get("name")
        password = request.POST.get("password")

        response = (
            supabase
            .table("admin")
            .select("*")
            .eq("name", name)
            .eq("password", password)
            .execute()
        )

        if len(response.data) > 0:

            request.session["admin_name"] = name

            return redirect("admin_dashboard")

        return render(
            request,
            "admin/adhome.html",
            {"error": "Invalid credentials"}
        )

    return render(request, "admin/adhome.html")
    
def admin_dashboard(request):
    return render(request, "admin/admin_dashboard.html")

def profile_update(request):

    current_admin = request.session.get("admin_name")

    if not current_admin:
        return redirect("admins")

    if request.method == "POST":

        new_name = request.POST.get("admin_name")
        new_password = request.POST.get("password")

        response = (
            supabase
            .table("admin")
            .update({
                "name": new_name,
                "password": new_password
            })
            .eq("name", current_admin)
            .execute()
        )

        request.session["admin_name"] = new_name

        return redirect("admin_dashboard")

    return render(request, "admin/profile_update.html")

def user_details_view(request):
    # Add logic here (e.g., fetching a list of users from the database)
    return render(request, 'admin/user_details.html')

def get_users(request):
    users = supabase.table("users").select("*").execute()
    return JsonResponse(users.data, safe=False)

def add_user(request):

    if request.method == "POST":

        data = json.loads(request.body)

        supabase.table("users").insert({
            "ktu_id": data["ktu_id"],
            "name": data["name"],
            "passout_year": data["passout_year"],
            "email": data["email"],
            "contact": data["contact"]
        }).execute()

        return JsonResponse({
            "message": "User Added"
        })

    return JsonResponse({
        "message": "Invalid Request"
    })

def update_user(request):

    if request.method == "PUT":

        data = json.loads(request.body)

        ktu_id = data["ktu_id"]

        supabase.table("users")\
            .update({
                "name": data["name"],
                "passout_year": data["passout_year"],
                "email": data["email"],
                "contact": data["contact"]
            })\
            .eq("ktu_id", ktu_id)\
            .execute()

        return JsonResponse({
            "message": "User updated successfully"
        })

    return JsonResponse({
        "message": "Invalid Request"
    })


def delete_user(request):

    if request.method == "DELETE":

        data = json.loads(request.body)

        supabase.table("users")\
            .delete()\
            .eq("ktu_id", data["ktu_id"])\
            .execute()

        return JsonResponse({
            "message": "User deleted successfully"
        })

    return JsonResponse({
        "message": "Invalid Request"
    })
