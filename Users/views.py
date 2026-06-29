from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404, redirect
from .models import tbl_blog
from .models import tbl_blog_like
from .models import tbl_blog_view
from Guest.models import tbl_user
from Users.models import tbl_blog_comment
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from Administrator.models import tbl_category
from django.utils.cache import add_never_cache_headers

def no_cache(view_func):
    def wrapper(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)
        add_never_cache_headers(response)
        return response
    return wrapper

def login_required_session(view_func):
    def wrapper(request, *args, **kwargs):
        if "uid" not in request.session:
            return redirect("/guest/Login/")

        response = view_func(request, *args, **kwargs)
        add_never_cache_headers(response)
        return response

    return wrapper

@login_required_session
def myprofile(request):
    data = tbl_user.objects.get(id=request.session["uid"])
    return render(request, "User/MyProfile.html", {"data": data})

@login_required_session
def editprofile(requests):
    return render(requests, "User/EditProfile.html")

@login_required_session
def change_password(request):
    if request.method == "GET":
        return render(request, "user/ChangePassword.html")

    if request.method == "POST":
        email = request.POST.get("user_email")
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = tbl_user.objects.filter(user_email=email).first()

        if not user:
            return render(request, "user/ChangePassword.html", {
                "msg": "Email not found"
            })

        if not check_password(old_password, user.password):
            return render(request, "user/ChangePassword.html", {
                "msg": "Old password is incorrect"
            })

        if new_password != confirm_password:
            return render(request, "user/ChangePassword.html", {
                "msg": "Passwords do not match"
            })

        user.password = make_password(new_password)
        user.save()

        return render(request, "user/ChangePassword.html", {
            "msg": "Password updated successfully"
        })

@login_required_session
def addblog(request):
    if "uid" not in request.session:
        return redirect("login")
    uid = request.session["uid"]
    user = tbl_user.objects.get(id=uid)
    if request.method == "POST":
        title = request.POST.get("title")
        blog = request.POST.get("blog")
        image = request.FILES.get("image")
        category = request.POST.get("category")
        tbl_blog.objects.create(
            blog_title=title,
            blog_content=blog,
            blog_image=image,
            user=user,
            category_id=category
        )
        return redirect("ViewBlog")
    category = tbl_category.objects.all()
    return render(request,"User/AddBlog.html",{"Category": category})

@login_required_session
def viewblog(request):

    blogs = tbl_blog.objects.all().order_by("-id")
    categories = tbl_category.objects.all()
    search = request.GET.get("search")
    category = request.GET.get("category")
    if search:
        blogs = blogs.filter(
            user__user_name__icontains=search
        )
    if category:
        blogs = blogs.filter(
            category_id=category
        )
    return render(
        request,
        "User/ViewBlog.html",
        {
            "blogs": blogs,
            "Category": categories
        }
    )

@login_required_session
def blogdetails(request, id):
    blog = get_object_or_404(tbl_blog, id=id)
    user = get_object_or_404(tbl_user, id=request.session["uid"])
    viewed = tbl_blog_view.objects.filter(user=user, blog=blog).first()
    if viewed is None:
        tbl_blog_view.objects.create(user=user, blog=blog)
        blog.blog_views += 1
        blog.save()
    return render(request, "User/BlogDetails.html", {"blog": blog})

@login_required_session
def user_HomePage(requests):
    return render(requests, "User/user_HomePage.html")

@login_required_session
def user_profile(request, id):
    data = tbl_user.objects.get(id=id)
    return render(request, "User/UserProfile.html", {"data": data})

@login_required_session
def user_blog_list(request, id):
    blogs = tbl_blog.objects.filter(user_id=id)
    return render(request, "User/ViewBlog.html", {"blogs": blogs})

@login_required_session
def like_blog(request, id):
    user_id = request.session.get("uid")
    if not user_id:
        return redirect("MyProfile")
    user = get_object_or_404(tbl_user, id=user_id)
    blog = get_object_or_404(tbl_blog, id=id)
    like_exists = tbl_blog_like.objects.filter(user=user, blog=blog).first()
    if like_exists:
        like_exists.delete()
    else:
        tbl_blog_like.objects.create(user=user, blog=blog)
    return redirect(request.META.get("HTTP_REFERER", "ViewBlog"))

@login_required_session
def add_comment(request, id):
    if request.method == "POST":
        user_id = request.session.get("uid")
        if not user_id:
            return redirect("MyProfile")
        user = get_object_or_404(tbl_user, id=user_id)
        blog = get_object_or_404(tbl_blog, id=id)
        comment_text = request.POST.get("comment")
        if comment_text:
            tbl_blog_comment.objects.create(
                user=user,
                blog=blog,
                comment=comment_text
            )
    return redirect("BlogDetails", id=id)

@login_required_session
def delete_comment(request, id):
    user_id = request.session.get("uid")
    if not user_id:
        return redirect("MyProfile")
    user = get_object_or_404(tbl_user, id=user_id)
    comment = get_object_or_404(tbl_blog_comment, id=id)
    if comment.user.id == user.id:
        comment.delete()
    return redirect(request.META.get("HTTP_REFERER", "ViewBlog"))

@login_required_session
def edit_comment(request, id):
    comment = get_object_or_404(tbl_blog_comment, id=id)
    if request.session.get("uid") != comment.user.id:
        return redirect("ViewBlog")
    if request.method == "POST":
        comment.comment = request.POST.get("comment")
        comment.save()
    return redirect(request.META.get("HTTP_REFERER"))

@login_required_session
def reply_comment(request, id):
    if request.method == "POST":
        user = get_object_or_404(tbl_user, id=request.session.get("uid"))
        parent_comment = get_object_or_404(tbl_blog_comment, id=id)
        comment_text = request.POST.get("comment")
        tbl_blog_comment.objects.create(user=user, blog=parent_comment.blog, comment=comment_text, parent=parent_comment)
    return redirect(request.META.get("HTTP_REFERER"))

@login_required_session
def logout(request):
    request.session.flush()
    return redirect("/guest/Login/")

@login_required_session
def delete_blog(request, id):
    if "uid" not in request.session:
        return redirect("login")
    blog = get_object_or_404(tbl_blog, id=id)
    if blog.user.id != request.session["uid"]:
        return redirect("BlogDetails", id=id)
    blog.delete()
    return redirect("ViewBlog")

@login_required_session
def edit_blog(request, id):
    if "uid" not in request.session:
        return redirect("login")
    blog = get_object_or_404(tbl_blog, id=id)
    if blog.user.id != request.session["uid"]:
        return redirect("ViewBlog")
    if request.method == "POST":
        blog.blog_title = request.POST.get("title")
        blog.blog_content = request.POST.get("blog")
        blog.category_id = request.POST.get("category")
        if request.FILES.get("image"):
            blog.blog_image = request.FILES.get("image")
        blog.save()
        return redirect("BlogDetails", id=blog.id)
    categories = tbl_category.objects.all()
    return render(
        request,
        "User/AddBlog.html",
        {
            "blog": blog,
            "Category": categories,
            "edit": True,
        }
    )