from django.shortcuts import render

def home(request):
    return render(request, "home/home.html")

def members(request):
    return render(request, "home/members.html")  

def admins(request):
    return render(request, "admin/adhome.html")    