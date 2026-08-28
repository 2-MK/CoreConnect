from django.shortcuts import render, redirect
from .supabase_client import supabase
from django.http import JsonResponse
from django.contrib import messages
from django.db import connection
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

import json
import random
import string
import bcrypt

from django.http import JsonResponse
from django.shortcuts import render

from .supabase_client import supabase



def add_user(request):

    if request.method == "POST":

        try:

            data = json.loads(request.body)

            # Generate random 4-character password
            default_password = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=4)
            )

            hashed_password = bcrypt.hashpw(
                default_password.encode(),
                bcrypt.gensalt()
            ).decode()

            supabase.table("users").insert({

                "ktu_id": data["ktu_id"],
                "name": data["name"],
                "passout_year": data.get("passout_year"),
                "email": data["email"],
                "ritemail": data.get("ritemail"),
                "contact": data.get("contact"),

                # hashed password for login
                "password": hashed_password,

                # plain password for admin reference
                "savedpassword": default_password

            }).execute()

            return JsonResponse({

                "message": "User added successfully.",
                "default_password": default_password

            })

        except Exception as e:
            return JsonResponse({
                "message": str(e)
            }, status=500)

    return JsonResponse({
        "message": "Invalid request"
    }, status=400)

def search_user(request, ktu_id):

    result = (
        supabase.table("users")
        .select("*")
        .eq("ktu_id", ktu_id)
        .execute()
    )

    if result.data:
        return JsonResponse(result.data[0], safe=False)

    return JsonResponse({"message": "User not found"}, status=404)


def delete_user(request, user_id):

    if request.method == "DELETE":

        supabase.table("users").delete().eq("id", user_id).execute()

        return JsonResponse({"message": "Deleted"})

    return JsonResponse({"message": "Invalid"}, status=400)

def update_user(request, user_id):

    if request.method != "PUT":

        return JsonResponse({

            "message": "Invalid request"

        }, status=400)

    try:

        data = json.loads(request.body)

        supabase.table("users").update({

            "name": data["name"],
            "passout_year": data["passout_year"],
            "email": data["email"],
            "ritemail": data["ritemail"],
            "contact": data["contact"]

        }).eq("id", user_id).execute()

        return JsonResponse({

            "message": "User updated successfully"

        })

    except Exception as e:

        return JsonResponse({

            "message": str(e)

        }, status=500)


def student_manage(request):
    return render(request, "admin/student_manage.html")

def alumni_approval(request):
    return render(request, "admin/alumni_approval.html")

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

    result = (
        supabase.table("users")
        .select("*")
        .eq("id", user_id)
        .execute()
    )

    user = result.data[0] if result.data else None

    if not user:
        return redirect("password_login")

    if request.method == "POST":

        email = request.POST.get("email")
        contact = request.POST.get("contact")
        parent_contact = request.POST.get("parent_contact")

        supabase.table("users").update({
            "email": email,
            "contact": contact,
            "parent_contact": parent_contact
        }).eq("id", user_id).execute()

        messages.success(request, "Profile updated successfully.")

        return redirect("user_profile_update")

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

    passout_year = ""
    name = ""
    ktu_id = ""

    search_query = None
    search_type = None

    if request.method == "POST":

        passout_year = request.POST.get("passout_year", "").strip()
        name = request.POST.get("name", "").strip()
        ktu_id = request.POST.get("ktu_id", "").strip()

        query = supabase.table("alumni_details").select("*")

        # Filter by Passout Year
        if passout_year:
            query = query.eq("passout_year", passout_year)
            search_type = "passout_year"
            search_query = passout_year

        # Optional Name filter
        if name:
            query = query.ilike("name", f"%{name}%")
            if not search_type:
                search_type = "name"
                search_query = name

        # Optional KTU ID filter
        if ktu_id:
            query = query.eq("ktu_id", ktu_id)
            if not search_type:
                search_type = "ktu_id"
                search_query = ktu_id

        response = query.order("passout_year").order("name").execute()
        alumni = response.data

    else:
        response = (
            supabase.table("alumni_details")
            .select("*")
            .order("passout_year")
            .order("name")
            .execute()
        )
        alumni = response.data

    return render(
        request,
        "admin/alumni_directory.html",
        {
            "alumni": alumni,
            "passout_year": passout_year,
            "name": name,
            "ktu_id": ktu_id,
            "search_query": search_query,
            "search_type": search_type,
        },
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

def dis_placedstd(request):
    # Fetch placed students
    placed_students = (
        supabase.table("placed_students")
        .select("*")
        .order("placement_date", desc=True)
        .execute()
    )
    context = {
        "placed_students": placed_students.data,
    }
    return render(request, "home/placement.html",context)


def dis_placement(request):
    

    # Fetch all placement opportunities (Active + Closed)
    placement_opportunities = (
        supabase.table("placement_opportunities")
        .select("*")
        .order("deadline", desc=False)
        .execute()
    )

    context = {
        
        "placement_opportunities": placement_opportunities.data,
    }

    return render(request, "user/placement.html", context)



from django.shortcuts import render
from django.http import HttpResponse
import csv


def student_manage(request):

    search = request.GET.get("search", "").strip()
    year = request.GET.get("year", "").strip()

    # Fetch all students
    result = supabase.table("users").select("*").order("name").execute()
    students = result.data if result.data else []

    # Search
    if search:
        students = [
            s for s in students
            if search.lower() in s["name"].lower()
            or search.lower() in s["ktu_id"].lower()
        ]

    # Filter by year
    if year:
        students = [
            s for s in students
            if s["passout_year"] == year
        ]

    # Download CSV
    if request.GET.get("download") == "1":

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="students.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Name",
            "KTU ID",
            "Saved Password"
        ])

        for s in students:
            writer.writerow([
                s["name"],
                s["ktu_id"],
                s["savedpassword"]
            ])

        return response

    # Get unique years
    years = sorted(
        list(
            set(
                student["passout_year"]
                for student in result.data
                if student["passout_year"]
            )
        )
    )

    return render(
        request,
        "admin/student_manage.html",
        {
            "students": students,
            "years": years,
            "search": search,
            "selected_year": year,
        },
    )

def alumni_approval(request):

    # Get available passout years
    year_response = (
        supabase.table("users")
        .select("passout_year")
        .not_.is_("passout_year", "null")
        .execute()
    )

    years = sorted(
        list(set([row["passout_year"] for row in year_response.data])),
        reverse=True
    )

    selected_year = request.GET.get("year")
    students = []

    if selected_year:

        student_response = (
            supabase.table("users")
            .select(
                "id,ktu_id,name,email,contact,alumni_approval"
            )
            .eq("passout_year", selected_year)
            .order("name")
            .execute()
        )

        students = student_response.data

    if request.method == "POST":

        # Approve One Student
        if "approve_student" in request.POST:

            student_id = request.POST.get("student_id")

            (
                supabase.table("users")
                .update({"alumni_approval": True})
                .eq("id", student_id)
                .execute()
            )

            return redirect(f"/alumni-approval/?year={selected_year}")

        # Approve All Students
        if "approve_all" in request.POST:

            (
                supabase.table("users")
                .update({"alumni_approval": True})
                .eq("passout_year", selected_year)
                .execute()
            )

            return redirect(f"/alumni-approval/?year={selected_year}")

    total = len(students)
    approved = sum(1 for s in students if s["alumni_approval"])

    context = {
        "years": years,
        "students": students,
        "selected_year": selected_year,
        "total": total,
        "approved": approved,
    }

    return render(request, "admin/alumni_approval.html", context)


def alumni_status(request):

    ktu_id = request.session.get("ktu_id")

    if not ktu_id:
        return redirect("login")

    user_res = (
        supabase.table("users")
        .select("*")
        .eq("ktu_id", ktu_id)
        .execute()
    )

    if not user_res.data:
        return render(request, "user/alumni_status.html", {
            "error": "User not found."
        })

    user = user_res.data[0]

    if not user["alumni_approval"]:
        return render(request, "user/alumni_status.html", {
            "approved": False
        })

    if request.method == "POST":

        email = request.POST.get("email")
        contact = request.POST.get("contact")
        designation = request.POST.get("designation")
        company_name = request.POST.get("company_name")

        data = {
            "ktu_id": user["ktu_id"],
            "name": user["name"],
            "email": email,
            "ritemail": user["ritemail"],
            "contact": contact,
            "passout_year": user["passout_year"],
            "designation": designation,
            "company_name": company_name,
        }

        existing = (
            supabase.table("alumni_details")
            .select("*")
            .eq("ktu_id", ktu_id)
            .execute()
        )

        if existing.data:
            (
                supabase.table("alumni_details")
                .update(data)
                .eq("ktu_id", ktu_id)
                .execute()
            )
        else:
            (
                supabase.table("alumni_details")
                .insert(data)
                .execute()
            )

        alumni = data

        return render(
            request,
            "user/alumni_status.html",
            {
                "approved": True,
                "user": user,
                "alumni": alumni,
                "success": "Alumni details saved successfully."
            }
        )

    details = (
        supabase.table("alumni_details")
        .select("*")
        .eq("ktu_id", ktu_id)
        .execute()
    )

    alumni = details.data[0] if details.data else {}

    return render(
        request,
        "user/alumni_status.html",
        {
            "approved": True,
            "user": user,
            "alumni": alumni
        }
    )

def events(request):

    # ---------------- DELETE ----------------
    delete_id = request.GET.get("delete")

    if delete_id:
        supabase.table("events").delete().eq("id", delete_id).execute()
        return redirect("events")

    # ---------------- EDIT ----------------
    edit_event = None
    edit_id = request.GET.get("edit")

    if edit_id:
        res = (
            supabase.table("events")
            .select("*")
            .eq("id", edit_id)
            .execute()
        )

        if res.data:
            edit_event = res.data[0]

    # ---------------- INSERT / UPDATE ----------------
    if request.method == "POST":

        data = {
            "event_name": request.POST.get("event_name"),
            "description": request.POST.get("description"),
            "category": request.POST.get("category"),
            "venue": request.POST.get("venue"),
            "event_date": request.POST.get("event_date"),
            "start_time": request.POST.get("start_time"),
            "end_time": request.POST.get("end_time"),
            "registration_deadline": request.POST.get("registration_deadline"),
            "max_participants": int(request.POST.get("max_participants")),
            "organizer": request.POST.get("organizer"),
        }

        event_id = request.POST.get("event_id")

        if event_id:
            (
                supabase.table("events")
                .update(data)
                .eq("id", event_id)
                .execute()
            )
        else:
            (
                supabase.table("events")
                .insert(data)
                .execute()
            )

        return redirect("events")

    events = (
        supabase.table("events")
        .select("*")
        .order("event_date")
        .execute()
    )

    return render(
        request,
        "admin/events.html",
        {
            "events": events.data,
            "edit_event": edit_event,
        },
    )

def user_events(request):

    ktu_id = request.session.get("ktu_id")

    events = (
        supabase.table("events")
        .select("*")
        .order("event_date")
        .execute()
    )

    registrations = (
        supabase.table("event_participants")
        .select("event_name")
        .eq("ktu_id", ktu_id)
        .execute()
    )

    registered_events = [
        row["event_name"]
        for row in registrations.data
    ]

    return render(
        request,
        "user/events.html",
        {
            "events": events.data,
            "registered_events": registered_events
        }
    )

def register_event(request, event_id):

    ktu_id = request.session.get("ktu_id")

    if not ktu_id:
        return redirect("password_login")

    user = (
        supabase.table("users")
        .select("*")
        .eq("ktu_id", ktu_id)
        .execute()
    )

    if not user.data:
        return redirect("user_events")

    user = user.data[0]

    event = (
        supabase.table("events")
        .select("*")
        .eq("id", event_id)
        .execute()
    )

    if not event.data:
        return redirect("user_events")

    event = event.data[0]

    check = (
        supabase.table("event_participants")
        .select("*")
        .eq("ktu_id", ktu_id)
        .eq("event_name", event["event_name"])
        .execute()
    )

    if check.data:
        return redirect("user_events")

    data = {

        "event_name": event["event_name"],

        "ktu_id": user["ktu_id"],

        "name": user["name"],

        "email": user["email"],

        "contact": user["contact"]

    }

    supabase.table("event_participants").insert(data).execute()

    return redirect("user_events")

def cancel_registration(request, event_name):

    ktu_id = request.session.get("ktu_id")

    (
        supabase.table("event_participants")
        .delete()
        .eq("ktu_id", ktu_id)
        .eq("event_name", event_name)
        .execute()
    )

    return redirect("user_events")

def view_participants(request):

    # Get unique event names
    event_response = (
        supabase.table("event_participants")
        .select("event_name")
        .execute()
    )

    event_names = sorted(
        list(
            set(
                item["event_name"]
                for item in event_response.data
            )
        )
    )

    selected_event = request.GET.get("event")

    participants = []

    if selected_event:

        response = (
            supabase.table("event_participants")
            .select("event_name,name,ktu_id,contact,email")
            .eq("event_name", selected_event)
            .execute()
        )

        participants = response.data

    return render(
        request,
        "admin/view_participants.html",
        {
            "events": event_names,
            "participants": participants,
            "selected_event": selected_event,
        },
    )

from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

def download_participants_pdf(request):

    event = request.GET.get("event")

    response = (
        supabase.table("event_participants")
        .select("event_name,name,ktu_id,contact,email")
        .eq("event_name", event)
        .execute()
    )

    pdf = HttpResponse(content_type="application/pdf")

    pdf["Content-Disposition"] = (
        f'attachment; filename="{event}_participants.pdf"'
    )

    doc = SimpleDocTemplate(pdf)

    data = [
        [
            "Event",
            "Name",
            "KTU ID",
            "Contact",
            "Email",
        ]
    ]

    for p in response.data:

        data.append([
            p["event_name"],
            p["name"],
            p["ktu_id"],
            p["contact"],
            p["email"],
        ])

    table = Table(data)

    table.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),colors.grey),
        ("TEXTCOLOR",(0,0),(-1,0),colors.white),
        ("GRID",(0,0),(-1,-1),1,colors.black),
        ("BACKGROUND",(0,1),(-1,-1),colors.beige),
        ("BOTTOMPADDING",(0,0),(-1,0),10),
    ]))

    doc.build([table])

    return pdf


import os
import uuid

from django.shortcuts import render, redirect
from django.contrib import messages
def study_materials(request):

    edit_id = request.GET.get("edit")
    edit_material = None

    if edit_id:
        result = (
            supabase.table("study_materials")
            .select("*")
            .eq("id", edit_id)
            .single()
            .execute()
        )

        if result.data:
            edit_material = result.data

    if request.method == "POST":

        material_id = request.POST.get("material_id")

        semester = request.POST.get("semester")
        subject = request.POST.get("subject")
        title = request.POST.get("title")
        description = request.POST.get("description")

        uploaded_file = request.FILES.get("file")

        # ----------------------------
        # UPDATE
        # ----------------------------
        if material_id:

            update_data = {
                "semester": semester,
                "subject": subject,
                "title": title,
                "description": description,
            }

            if uploaded_file:

                extension = uploaded_file.name.split(".")[-1]
                unique_name = f"{uuid.uuid4()}.{extension}"

                path = f"{semester}/{subject}/{unique_name}"

                file_bytes = uploaded_file.read()

                supabase.storage.from_("study-materials").upload(
                    path,
                    file_bytes,
                    {
                        "content-type": uploaded_file.content_type
                    }
                )

                file_url = supabase.storage.from_("study-materials").get_public_url(path)

                update_data["file_name"] = uploaded_file.name
                update_data["file_url"] = file_url

            (
                supabase.table("study_materials")
                .update(update_data)
                .eq("id", material_id)
                .execute()
            )

            messages.success(request, "Material Updated Successfully")

            return redirect("study_materials")

        # ----------------------------
        # INSERT
        # ----------------------------
        else:

            if uploaded_file:

                extension = uploaded_file.name.split(".")[-1]

                unique_name = f"{uuid.uuid4()}.{extension}"

                path = f"{semester}/{subject}/{unique_name}"

                file_bytes = uploaded_file.read()

                supabase.storage.from_("study-materials").upload(
                    path,
                    file_bytes,
                    {
                        "content-type": uploaded_file.content_type
                    }
                )

                file_url = supabase.storage.from_("study-materials").get_public_url(path)

                supabase.table("study_materials").insert({

                    "semester": semester,
                    "subject": subject,
                    "title": title,
                    "description": description,
                    "file_name": uploaded_file.name,
                    "file_url": file_url

                }).execute()

                messages.success(request, "Material Uploaded Successfully")

                return redirect("study_materials")

    materials = (
        supabase.table("study_materials")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    context = {
        "materials": materials.data,
        "edit_material": edit_material
    }

    return render(request, "admin/study_materials.html", context)
def delete_study_material(request, id):

    supabase.table("study_materials").delete().eq("id", id).execute()

    messages.success(request, "Material Deleted Successfully")

    return redirect("study_materials")

def view_study_materials(request):

    semester = request.GET.get("semester", "").strip()
    subject = request.GET.get("subject", "").strip()
    title = request.GET.get("title", "").strip()

    query = supabase.table("study_materials").select("*")

    # Apply filters only if they are provided

    if semester:
        query = query.eq("semester", semester)

    if subject:
        query = query.eq("subject", subject)

    if title:
        query = query.ilike("title", f"%{title}%")

    materials = query.order("created_at", desc=True).execute()

    return render(
        request,
        "home/view_study_materials.html",
        {
            "materials": materials.data,
            "selected_semester": semester,
            "selected_subject": subject,
            "title": title,
        },
    )

def fund_management(request):

    # =========================
    # ADD STUDY MATERIAL
    # =========================
    if request.method == "POST":

        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()
        uploaded_file = request.FILES.get("file")

        if not title:
            messages.error(request, "Title is required.")
            return redirect("fund_management")

        if not uploaded_file:
            messages.error(request, "Please select a file.")
            return redirect("fund_management")

        try:
            # Create unique filename
            original_name = uploaded_file.name
            extension = os.path.splitext(original_name)[1]

            file_name = f"{uuid.uuid4()}{extension}"

            # Path inside the fund bucket
            file_path = f"study_materials/{file_name}"

            # Read file
            file_data = uploaded_file.read()

            # =========================
            # UPLOAD TO SUPABASE BUCKET
            # =========================
            supabase.storage.from_("fund").upload(
                file_path,
                file_data,
                {
                    "content-type": uploaded_file.content_type
                }
            )

            # =========================
            # GET PUBLIC URL
            # =========================
            file_url = supabase.storage.from_("fund").get_public_url(
                file_path
            )

            # =========================
            # SAVE DATA TO TABLE
            # =========================
            supabase.table("fund_management").insert({
                "title": title,
                "description": description,
                "file_url": file_url
            }).execute()

            messages.success(
                request,
                "Study material uploaded successfully."
            )

        except Exception as e:
            messages.error(
                request,
                f"Upload failed: {str(e)}"
            )

        return redirect("fund_management")

    # =========================
    # GET ALL MATERIALS
    # =========================
    try:
        response = (
            supabase
            .table("fund_management")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        materials = response.data or []

    except Exception as e:
        materials = []
        messages.error(
            request,
            f"Could not load materials: {str(e)}"
        )

    return render(
        request,
        "admin/fund_management.html",
        {
            "materials": materials
        }
    )

def delete_fund_management(request, material_id):

    if request.method != "POST":
        return redirect("fund_management")

    try:
        # Get the fund record
        response = (
            supabase
            .table("fund_management")
            .select("*")
            .eq("id", material_id)
            .single()
            .execute()
        )

        material = response.data

        if not material:
            messages.error(request, "Fund document not found.")
            return redirect("fund_mangement")

        file_url = material.get("file_url")

        # --------------------------------
        # Delete PDF from "fund" bucket
        # --------------------------------
        if file_url:

            marker = "/storage/v1/object/public/fund/"

            if marker in file_url:

                file_path = file_url.split(marker, 1)[1]

                supabase.storage \
                    .from_("fund") \
                    .remove([file_path])

        # --------------------------------
        # Delete database record
        # --------------------------------
        supabase.table("fund_management") \
            .delete() \
            .eq("id", material_id) \
            .execute()

        messages.success(
            request,
            "Fund document deleted successfully."
        )

    except Exception as e:

        messages.error(
            request,
            f"Delete failed: {str(e)}"
        )

    return redirect("fund_management")

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .supabase_client import supabase


def view_fund(request):
    """
    Display all fund records as cards.
    """

    try:
        response = (
            supabase
            .table("fund_management")
            .select("*")
            .order("created_at", desc=True)
            .execute()
        )

        funds = response.data or []

        return render(
            request,
            "user/view_fund.html",
            {
                "funds": funds
            }
        )

    except Exception as e:
        print("Fund fetch error:", e)

        return render(
            request,
            "user/view_fund.html",
            {
                "funds": [],
                "error": "Unable to load fund details."
            }
        )


def fund_detail(request, fund_id):
    """
    Display the selected fund's file.
    """

    try:
        response = (
            supabase
            .table("fund_management")
            .select("*")
            .eq("id", fund_id)
            .single()
            .execute()
        )

        fund = response.data

        if not fund:
            return HttpResponse("Fund not found.", status=404)

        return render(
            request,
            "user/fund_detail.html",
            {
                "fund": fund
            }
        )

    except Exception as e:
        print("Fund detail error:", e)
        return HttpResponse("Fund not found.", status=404)
    



def ptaupdates(request):
    selected_year = request.GET.get("year", "")

    # Get available years
    users_response = (
        supabase
        .table("users")
        .select("name, ktu_id, passout_year")
        .order("passout_year")
        .execute()
    )

    all_users = users_response.data or []

    # Get unique years
    years = sorted(
        {
            user["passout_year"]
            for user in all_users
            if user.get("passout_year")
        }
    )

    # Filter students by selected year
    if selected_year:
        students = [
            user for user in all_users
            if user.get("passout_year") == selected_year
        ]
    else:
        students = []

    context = {
        "students": students,
        "years": years,
        "selected_year": selected_year,
    }

    return render(request, "admin/ptaupdates.html", context)


def ptaupdates(request):

    selected_year = request.GET.get("year", "")

    response = (
        supabase
        .table("users")
        .select("name, ktu_id, passout_year")
        .order("name")
        .execute()
    )

    all_users = response.data or []

    years = sorted(
        {
            user["passout_year"]
            for user in all_users
            if user.get("passout_year")
        }
    )

    if selected_year:
        students = [
            user for user in all_users
            if user.get("passout_year") == selected_year
        ]
    else:
        students = []

    return render(
        request,
        "admin/ptaupdates.html",
        {
            "students": students,
            "years": years,
            "selected_year": selected_year,
        }
    )


def update_insights(request, ktu_id):

    # --------------------------------
    # GET STUDENT FROM USERS TABLE
    # --------------------------------

    student_response = (
        supabase
        .table("users")
        .select("name, ktu_id")
        .eq("ktu_id", ktu_id)
        .single()
        .execute()
    )

    student = student_response.data

    if not student:
        messages.error(request, "Student not found.")
        return redirect("ptaupdates")


    # --------------------------------
    # GET EXISTING INSIGHTS
    # --------------------------------

    insights_response = (
        supabase
        .table("insights")
        .select("*")
        .eq("ktu_id", ktu_id)
        .order("semester")
        .execute()
    )

    insights = insights_response.data or []


    # --------------------------------
    # SAVE DATA
    # --------------------------------

    if request.method == "POST":

        subjects = request.POST.getlist("subject_code")

        for subject_code in subjects:

            semester = request.POST.get(
                f"semester_{subject_code}"
            )

            subject_name = request.POST.get(
                f"subject_name_{subject_code}"
            )

            internal = request.POST.get(
                f"internal_{subject_code}"
            )

            external = request.POST.get(
                f"external_{subject_code}"
            )

            attendance = request.POST.get(
                f"attendance_{subject_code}"
            )


            data = {
                "ktu_id": student["ktu_id"],
                "name": student["name"],
                "semester": int(semester),
                "subject_code": subject_code,
                "subject_name": subject_name,
                "internal": internal if internal else None,
                "external": external if external else None,
                "attendance": attendance if attendance else None,
            }


            # Check existing record

            existing_response = (
                supabase
                .table("insights")
                .select("id")
                .eq("ktu_id", student["ktu_id"])
                .eq("semester", int(semester))
                .eq("subject_code", subject_code)
                .execute()
            )


            if existing_response.data:

                insight_id = existing_response.data[0]["id"]

                (
                    supabase
                    .table("insights")
                    .update(data)
                    .eq("id", insight_id)
                    .execute()
                )

            else:

                (
                    supabase
                    .table("insights")
                    .insert(data)
                    .execute()
                )


        messages.success(
            request,
            "Student insights updated successfully."
        )

        return redirect("ptaupdates")


    # --------------------------------
    # DISPLAY PAGE
    # --------------------------------

    return render(
        request,
        "admin/update_insights.html",
        {
            "student": student,
            "insights": insights,
        }
    )


def insights_search(request):
    student = None
    insights = []
    error = None

    name = request.GET.get("name", "").strip()
    ktu_id = request.GET.get("ktu_id", "").strip()

    # Both Name and KTU ID are required
    if name or ktu_id:

        if not name or not ktu_id:
            error = "Please enter both Student Name and KTU ID."

        else:
            # Verify BOTH name and KTU ID
            user_response = (
                supabase
                .table("users")
                .select("ktu_id, name")
                .eq("ktu_id", ktu_id)
                .ilike("name", name)
                .execute()
            )

            # Only show results when BOTH are correct
            if user_response.data:

                student = user_response.data[0]

                # Get insights only after successful verification
                insights_response = (
                    supabase
                    .table("insights")
                    .select(
                        "semester, subject_code, subject_name, "
                        "internal, external, attendance, created_at"
                    )
                    .eq("ktu_id", student["ktu_id"])
                    .order("semester")
                    .order("subject_code")
                    .execute()
                )

                insights = insights_response.data

            else:
                error = "Name and KTU ID do not match. Please check your details."

    return render(
        request,
        "home/insights_search.html",
        {
            "student": student,
            "insights": insights,
            "error": error,
            "searched_name": name,
            "searched_ktu_id": ktu_id,
        },
    )