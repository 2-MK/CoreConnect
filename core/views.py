from django.shortcuts import render, redirect
from .supabase_client import supabase
from django.http import JsonResponse
from django.contrib import messages
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



import bcrypt


def user_login(request):

    print("METHOD:", request.method)

    if request.method == "POST":

        ktu_id = request.POST.get("ktu_id")
        name = request.POST.get("name")

        print("KTU ID:", ktu_id)
        print("NAME:", name)

        result = (
            supabase.table("users")
            .select("*")
            .eq("ktu_id", ktu_id)
            .eq("name", name)
            .execute()
        )

        print("RESULT:", result.data)

        if not result.data:
            return render(
                request,
                "user/user_login.html",
                {"error": "Invalid KTU ID or Name"}
            )

        user = result.data[0]

        print("USER FOUND:", user)

        request.session["user_id"] = user["id"]

        # First-time login
        if not user.get("password"):
            print("Redirecting to set_password")
            return redirect("set_password")

        # Password already exists
        print("Redirecting to password_login")
        return redirect("password_login")

    return render(request, "user/user_login.html")


def set_password(request):

    if "user_id" not in request.session:
        return redirect("user_login")

    if request.method == "POST":

        password = request.POST.get("password")
        confirm = request.POST.get("confirm_password")

        if password != confirm:
            return render(
                request,
                "user/set_password.html",
                {"error": "Passwords do not match"}
            )

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        (
            supabase.table("users")
            .update({"password": hashed})
            .eq("id", request.session["user_id"])
            .execute()
        )

        return redirect("password_login")

    return render(request, "user/set_password.html")


def password_login(request):

    if request.method == "POST":

        ktu_id = request.POST.get("ktu_id")
        password = request.POST.get("password")

        result = (
            supabase.table("users")
            .select("*")
            .eq("ktu_id", ktu_id)
            .execute()
        )

        if result.data:

            user = result.data[0]

            if (
                user.get("password")
                and bcrypt.checkpw(
                    password.encode(),
                    user["password"].encode()
                )
            ):

                request.session["user_id"] = user["id"]
                request.session["user_name"] = user["name"]
                request.session["ktu_id"] = user["ktu_id"]

                return redirect("/dashboard/")

        return render(
            request,
            "user/password_login.html",
            {"error": "Invalid Credentials"}
        )

    return render(request, "user/password_login.html")


def user_dashboard(request):

    if "user_id" not in request.session:
        return redirect("password_login")

    return render(
        request,
        "user/user_dashboard.html",
        {
            "name": request.session.get("user_name"),
            "ktu_id": request.session.get("ktu_id")
        }
    )


def change_password(request):

    if "user_id" not in request.session:
        return redirect("password_login")

    if request.method == "POST":

        password = request.POST.get("password")

        hashed = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        (
            supabase.table("users")
            .update({"password": hashed})
            .eq("id", request.session["user_id"])
            .execute()
        )

        return redirect("user_dashboard")

    return render(
        request,
        "user/change_password.html"
    )


def user_profile_update(request):

    if "user_id" not in request.session:
        return redirect("password_login")

    user_id = request.session.get("user_id")

    # Fetch current user data
    result = supabase.table("users").select("*").eq("id", user_id).execute()
    user = result.data[0] if result.data else None

    if not user:
        return redirect("password_login")

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        designation = request.POST.get("designation")
        company_name = request.POST.get("company_name")

        supabase.table("users").update({
            "name": name,
            "email": email,
            "contact": contact,
            "designation": designation,
            "company_name": company_name
        }).eq("id", user_id).execute()

        request.session["user_name"] = name
        
        messages.success(request, "Profile updated successfully")

        return redirect("user_dashboard")

    return render(
        request,
        "user/profile_update.html",
        {
            "user": user
        }
    )


def user_logout(request):

    request.session.flush()

    return redirect("password_login")


def alumni_directory(request):
    
    if not request.session.get("admin_name"):
        return redirect("admins")
    
    alumni = []
    search_query = None
    search_type = None
    passout_year = ""
    name = ""
    ktu_id = ""
    
    if request.method == "POST":
        search_type = request.POST.get("search_type")
        search_query = request.POST.get("search_query")
        passout_year = request.POST.get("passout_year", "").strip()
        name = request.POST.get("name", "").strip()
        ktu_id = request.POST.get("ktu_id", "").strip()

        if passout_year:
            search_type = "passout_year"
            search_query = passout_year
            response = (
                supabase.table("users")
                .select("*")
                .eq("passout_year", search_query)
                .execute()
            )
        elif name:
            search_type = "name"
            search_query = name
            response = (
                supabase.table("users")
                .select("*")
                .ilike("name", f"%{search_query}%")
                .execute()
            )
        elif ktu_id:
            search_type = "ktu_id"
            search_query = ktu_id
            response = (
                supabase.table("users")
                .select("*")
                .eq("ktu_id", search_query)
                .execute()
            )
        elif search_type and search_query:
            if search_type == "passout_year":
                response = (
                    supabase.table("users")
                    .select("*")
                    .eq("passout_year", search_query)
                    .execute()
                )
            elif search_type == "name":
                response = (
                    supabase.table("users")
                    .select("*")
                    .ilike("name", f"%{search_query}%")
                    .execute()
                )
            elif search_type == "ktu_id":
                response = (
                    supabase.table("users")
                    .select("*")
                    .eq("ktu_id", search_query)
                    .execute()
                )
            else:
                response = None
        else:
            response = None
            
        alumni = response.data if response else []
    
    return render(
        request,
        "admin/alumni_directory.html",
        {
            "alumni": alumni,
            "search_query": search_query,
            "search_type": search_type,
            "passout_year": passout_year,
            "name": name,
            "ktu_id": ktu_id,
        }
    )

def placement_management(request):
    return render(request, 'admin/placement.html')


def placement_opportunities(request):
    opportunities = []
    editing_opportunity = None

    if request.method == "POST":
        action = request.POST.get("action")
        opportunity_id = request.POST.get("id")

        try:
            if action == "delete":
                supabase.table("placement_opportunities").delete().eq("id", opportunity_id).execute()
                messages.success(request, "Opportunity deleted successfully.")
            elif action == "update":
                update_data = {
                    "company_name": request.POST.get("company_name"),
                    "role": request.POST.get("role"),
                    "eligibility": request.POST.get("eligibility"),
                    "deadline": request.POST.get("deadline") or None,
                    "description": request.POST.get("description"),
                    "status": request.POST.get("status") or "Active",
                }
                supabase.table("placement_opportunities").update(update_data).eq("id", opportunity_id).execute()
                messages.success(request, "Opportunity updated successfully.")
            elif action == "create":
                insert_data = {
                    "company_name": request.POST.get("company_name"),
                    "role": request.POST.get("role"),
                    "eligibility": request.POST.get("eligibility"),
                    "deadline": request.POST.get("deadline") or None,
                    "description": request.POST.get("description"),
                    "status": request.POST.get("status") or "Active",
                }
                supabase.table("placement_opportunities").insert(insert_data).execute()
                messages.success(request, "Opportunity created successfully.")
            else:
                messages.error(request, "Invalid action.")
        except Exception as exc:
            messages.error(request, f"Unable to process opportunity: {exc}")

        return redirect("placement_opportunities")

    edit_id = request.GET.get("edit_id")
    if edit_id:
        response = supabase.table("placement_opportunities").select("*").eq("id", edit_id).execute()
        if response.data:
            editing_opportunity = response.data[0]

    response = supabase.table("placement_opportunities").select("*").order("created_at", desc=True).execute()
    opportunities = response.data if response.data else []

    return render(
        request,
        "admin/placement_opportunities.html",
        {
            "opportunities": opportunities,
            "editing_opportunity": editing_opportunity,
        },
    )

def placement_achievements(request):
    return render(request, 'admin/placement_achievements.html')

import os
import uuid
import tempfile

from django.shortcuts import render, redirect


def _upload_placement_image(image):
    if not image:
        return None

    filename = f"{uuid.uuid4()}_{image.name}"
    extension = os.path.splitext(image.name)[1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=extension) as temp:
        for chunk in image.chunks():
            temp.write(chunk)
        temp_path = temp.name

    try:
        supabase.storage.from_("placement-images").upload(
            path=filename,
            file=temp_path,
            file_options={"content-type": image.content_type},
        )
        return supabase.storage.from_("placement-images").get_public_url(filename)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)


def placement_updates(request):

    if request.method == "POST":

        try:

            student_name = request.POST.get("student_name")
            company_name = request.POST.get("company_name")
            job_role = request.POST.get("job_role")
            package_lpa = request.POST.get("package_lpa")
            placement_date = request.POST.get("placement_date")
            caption = request.POST.get("caption")

            image = request.FILES.get("achievement_image")

            image_url = _upload_placement_image(image)

            # Insert into table
            response = (
                supabase.table("placed_students")
                .insert({
                    "student_name": student_name,
                    "company_name": company_name,
                    "job_role": job_role,
                    "package_lpa": float(package_lpa) if package_lpa else None,
                    "placement_date": placement_date if placement_date else None,
                    "caption": caption,
                    "image_url": image_url
                })
                .execute()
            )

            print(response)

            return render(
                request,
                "admin/placement_achievements.html",
                {
                    "success_message": "Placement saved successfully."
                }
            )

        except Exception as e:

            print("ERROR:", e)

            return render(
                request,
                "admin/placement_achievements.html",
                {
                    "error_message": str(e)
                }
            )

    return render(
        request,
        "admin/placement_achievements.html"
    )

def manage_placement(request):
    placements = []
    editing_placement = None

    if request.method == "POST":
        action = request.POST.get("action")
        placement_id = request.POST.get("id")

        try:
            if action == "delete":
                supabase.table("placed_students").delete().eq("id", placement_id).execute()
                messages.success(request, "Placement record deleted successfully.")
            elif action == "update":
                update_data = {
                    "student_name": request.POST.get("student_name"),
                    "company_name": request.POST.get("company_name"),
                    "job_role": request.POST.get("job_role"),
                    "package_lpa": float(request.POST.get("package_lpa")) if request.POST.get("package_lpa") else None,
                    "placement_date": request.POST.get("placement_date") or None,
                    "caption": request.POST.get("caption"),
                }

                image = request.FILES.get("achievement_image")
                if image:
                    update_data["image_url"] = _upload_placement_image(image)

                supabase.table("placed_students").update(update_data).eq("id", placement_id).execute()
                messages.success(request, "Placement record updated successfully.")
            elif action == "create":
                insert_data = {
                    "student_name": request.POST.get("student_name"),
                    "company_name": request.POST.get("company_name"),
                    "job_role": request.POST.get("job_role"),
                    "package_lpa": float(request.POST.get("package_lpa")) if request.POST.get("package_lpa") else None,
                    "placement_date": request.POST.get("placement_date") or None,
                    "caption": request.POST.get("caption"),
                }

                image = request.FILES.get("achievement_image")
                if image:
                    insert_data["image_url"] = _upload_placement_image(image)

                supabase.table("placed_students").insert(insert_data).execute()
                messages.success(request, "Placement record created successfully.")
            else:
                messages.error(request, "Invalid action.")
        except Exception as exc:
            messages.error(request, f"Unable to process placement: {exc}")

        return redirect("manage_placement")

    edit_id = request.GET.get("edit_id")
    if edit_id:
        response = supabase.table("placed_students").select("*").eq("id", edit_id).execute()
        if response.data:
            editing_placement = response.data[0]

    response = supabase.table("placed_students").select("*").order("created_at", desc=True).execute()
    placements = response.data if response.data else []

    return render(
        request,
        "admin/placement_management.html",
        {
            "placements": placements,
            "editing_placement": editing_placement,
        },
    )


def dis_placement(request):
    # Fetch placed students
    placed_students = (
        supabase.table("placed_students")
        .select("*")
        .order("placement_date", desc=True)
        .execute()
    )

    # Fetch all placement opportunities (Active + Closed)
    placement_opportunities = (
        supabase.table("placement_opportunities")
        .select("*")
        .order("deadline", desc=False)
        .execute()
    )

    context = {
        "placed_students": placed_students.data,
        "placement_opportunities": placement_opportunities.data,
    }

    return render(request, "home/placement.html", context)