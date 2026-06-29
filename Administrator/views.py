from django.shortcuts import render
from Administrator.models import *
from django.shortcuts import redirect
from Guest.models import tbl_user
from Users.models import tbl_blog
from django.shortcuts import get_object_or_404
from django.db.models import Count
from datetime import datetime
from Users.models import tbl_blog_like
from django.utils.decorators import decorator_from_middleware
from django.middleware.cache import CacheMiddleware
from django.utils.cache import add_never_cache_headers


def no_cache(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        add_never_cache_headers(response)
        return response
    return wrapper


def admin_login_required(view_func):
    def wrapper(request, *args, **kwargs):

        if "uid" not in request.session:
            return redirect("/guest/Login/")

        response = view_func(request, *args, **kwargs)
        add_never_cache_headers(response)
        return response

    return wrapper

@admin_login_required
def HomePage(request):

    total_users = tbl_user.objects.count()
    total_blogs = tbl_blog.objects.count()
    top_blogs = (tbl_blog.objects.annotate(total_likes=Count("tbl_blog_like")).order_by("-total_likes"))
    highest = top_blogs.first()
    if highest:
        top_blogs = top_blogs.filter(total_likes=highest.total_likes)
    else:
        top_blogs = []
    return render(
        request,
        "Administrator/HomePage.html",
        {
            "total_users": total_users,
            "total_blogs": total_blogs,
            "top_blogs": top_blogs,
        },
    )

@admin_login_required
def userverification(requests):
    return render(requests, "Administrator/UserVerification.html")

@admin_login_required
def category(requests):
    if requests.method == "POST":
        category_name = requests.POST.get("category")

        if category_name and category_name.strip():
            tbl_category.objects.create(category_name=category_name)

        return redirect("Category")
    data = tbl_category.objects.all()
    return render(requests, "Administrator/Category.html", {"Category": data})

@admin_login_required
def delete_category(requests, id):
    data = get_object_or_404(tbl_category, id=id)
    data.delete()
    return redirect("Category")

@admin_login_required
def adminregistration(requests):
    if requests.method == "POST":
        admin_name = requests.POST.get("admin_name")
        admin_email = requests.POST.get("admin_email")
        admin_password = requests.POST.get("admin_password")
        if admin_name and admin_email and admin_password:
            tbl_admin.objects.create(admin_name=admin_name, admin_email=admin_email, admin_password=admin_password)
        return redirect("adminregistration")
    data = tbl_admin.objects.all()
    return render(requests, "Administrator/adminregistration.html", {"AdminRegistration": data})

@admin_login_required
def delete_admin_registration(requests, id):
    data = get_object_or_404(tbl_admin, id=id)
    data.delete()
    return redirect("adminregistration")

@admin_login_required
def user_verification(requests):
    users = tbl_user.objects.all()
    return render(requests, "Administrator/UserVerification.html", {"users": users})

@admin_login_required
def view_user_blog(request, id):
    blogs = tbl_blog.objects.filter(user_id=id).order_by("-id")
    user = tbl_user.objects.get(id=id)
    return render(request, "Administrator/ViewUserBlog.html", {
        "blogs": blogs,
        "user": user
    })  

@admin_login_required
def view_user_blog_details(request, id):
    blog = get_object_or_404(tbl_blog, id=id)
    return render(request, "Administrator/ViewUserBlogDetails.html", {"blog": blog})

@admin_login_required
def admin_logout(request):
    request.session.flush()
    return redirect("/guest/Login/")

@admin_login_required
def ViewAllBlogs(request):
    blogs = (
        tbl_blog.objects
        .annotate(total_likes=Count("tbl_blog_like"))
        .order_by("-id")
    )
    return render(
        request,
        "Administrator/ViewAllBlogs.html",
        {
            "blogs": blogs
        }
    )

@admin_login_required
def Reports(request):
    users = tbl_user.objects.all()
    blogs = tbl_blog.objects.all()
    from_date = request.GET.get("from_date")
    to_date = request.GET.get("to_date")
    if from_date and to_date:
        users = users.filter(
            joined_date__date__range=[from_date, to_date]
        )
        blogs = blogs.filter(
            blog_date__range=[from_date, to_date]
        )
    top_blogs = (
        blogs
        .annotate(total_likes=Count("tbl_blog_like"))
        .order_by("-total_likes")[:3]
    )
    active_users = (
        tbl_user.objects
        .annotate(blog_count=Count("tbl_blog"))
        .order_by("-blog_count")[:3]
    )
    context = {
        "users": users,
        "blogs": blogs,
        "top_blogs": top_blogs,
        "active_users": active_users,
        "total_users": users.count(),
        "total_blogs": blogs.count(),
        "from_date": from_date,
        "to_date": to_date,
    }
    return render(
        request,
        "Administrator/Reports.html",
        context
    )
