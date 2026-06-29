from django.urls import path
from . import views

urlpatterns = [
    path('MyProfile/', views.myprofile, name = "MyProfile"),    
    path('EditProfile/', views.editprofile, name = "EditProfile"),
    path('ChangePassword/', views.change_password, name = "ChangePassword"),
    path('AddBlog/', views.addblog, name = "AddBlog"),
    path('ViewBlog/', views.viewblog, name = "ViewBlog"),
    path('user_HomePage/', views.user_HomePage, name = "user_HomePage"),
    path('BlogDetails/<int:id>/', views.blogdetails, name='BlogDetails'),
    path('UserProfile/<int:id>/', views.user_profile, name='user_profile'),
    path('UserBlogs/<int:id>/', views.user_blog_list, name='user_blog_list'),
    path('LikeBlog/<int:id>/', views.like_blog, name='like_blog'),
    path('AddComment/<int:id>/', views.add_comment, name='add_comment'),
    path('DeleteComment/<int:id>/', views.delete_comment, name='delete_comment'),
    path('EditComment/<int:id>/', views.edit_comment, name='edit_comment'),
    path('reply_comment/<int:id>/', views.reply_comment, name='reply_comment'),
    path("Logout/", views.logout, name="Logout"),
    path("DeleteBlog/<int:id>/", views.delete_blog, name="delete_blog"),
    path("editblog/<int:id>/", views.edit_blog, name="edit_blog"),
]