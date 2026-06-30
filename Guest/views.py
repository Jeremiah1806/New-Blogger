from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404, redirect
from Guest.models import tbl_user
from Administrator.models import tbl_admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def delete_user(request, id):
    user = get_object_or_404(tbl_user, id=id)
    user.delete()
    return redirect("user_registration")

def userregistration(requests):
    return render(requests, "Guest/UserRegistration.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = tbl_user.objects.get(user_email=email, user_password=password)

            request.session["uid"] = user.id
            request.session["uname"] = user.user_name

            return redirect("/administrator/HomePage/")

        except tbl_user.DoesNotExist:
            return render(request, "Guest/Login.html", {"msg": "Invalid credentials"})

    return render(request, "Guest/Login.html")

def userregistration(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        contact = request.POST.get("contact")
        place = request.POST.get("place")
        dob = request.POST.get("dob")

        photo = request.FILES.get("photo")


        tbl_user.objects.create(
            user_name=name,
            user_email=email,
            user_password=password,
            user_gender=gender,
            user_contact=contact,
            user_place=place,
            user_dateofbirth=dob,
            user_photo=photo
        )


        return redirect("login")


    return render(request,"Guest/UserRegistration.html")

def delete_user(request, id):
    user = get_object_or_404(tbl_user, id=id)
    user.delete()
    return redirect("userregistration") 

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        admin = tbl_admin.objects.filter(admin_email=email, admin_password=password).first()
        if admin:
            request.session["uid"] = admin.id
            request.session["name"] = admin.admin_name
            return redirect("homepage")   
        user = tbl_user.objects.filter(user_email=email, user_password=password).first()
        if user:
            request.session["uid"] = user.id
            request.session["name"] = user.user_name
            return redirect("user_HomePage") 
        return render(request, "Guest/login.html", {"msg": "Invalid credentials"})

    return render(request, "Guest/login.html")