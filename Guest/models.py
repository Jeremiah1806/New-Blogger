from django.db import models

# Create your models here.
class tbl_user(models.Model):
    user_name = models.CharField(max_length=50)
    user_email = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_photo = models.ImageField(upload_to="user_images/", blank=True, null=True)
    user_place = models.CharField(max_length=200)
    user_contact = models.CharField(max_length=10)
    user_gender = models.CharField(max_length=10)
    user_dateofbirth = models.CharField(max_length=10)
    joined_date = models.DateTimeField(auto_now_add=True,blank=True, null=True)