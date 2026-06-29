from django.urls import path
from . import views

urlpatterns = [
    path('HomePage/', views.HomePage, name = "homepage"),
    path('UserVerification/', views.user_verification, name="user_verification"),
    path('Category/', views.category, name = "Category"),
    path('delete_category/<int:id>/', views.delete_category, name = "delete_category"),
    path('AdminRegistration/', views.adminregistration, name = "adminregistration"),
    path('delete_admin_registration/<int:id>/', views.delete_admin_registration, name="delete_admin_registration"),
    path('ViewUserBlog/<int:id>/', views.view_user_blog, name='ViewUserBlog'),
    path('ViewUserBlogDetails/<int:id>/', views.view_user_blog_details,name='ViewUserBlogDetails'),
    path("logout/", views.admin_logout, name="admin_logout"),
    path("ViewAllBlogs/", views.ViewAllBlogs, name="ViewAllBlogs"),
    path("Reports/", views.Reports, name="Reports"),
]
