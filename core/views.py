from django.shortcuts import render, redirect
from .supabase_client import supabase

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