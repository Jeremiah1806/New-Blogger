from django.db import models

# Create your models here.
class tbl_admin(models.Model):
    admin_name = models.CharField(max_length=50)
    admin_email = models.CharField(max_length=50)
    admin_password = models.CharField(max_length=50)

class tbl_category(models.Model):
    category_name = models.CharField(max_length=50)


