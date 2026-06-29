from django.db import models
from Guest.models import tbl_user

from Administrator.models import tbl_category

class tbl_blog(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_content = models.TextField()
    blog_image = models.ImageField(upload_to="blog_images/", null=True, blank=True)
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    category = models.ForeignKey(tbl_category,on_delete=models.CASCADE,null=True,blank=True)
    blog_date = models.DateField(auto_now_add=True,null=True,blank=True)
    blog_views = models.IntegerField(default=0)

class tbl_blog_view(models.Model):
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    blog = models.ForeignKey(tbl_blog, on_delete=models.CASCADE)
    class Meta:
        unique_together = ("user", "blog")

class tbl_blog_like(models.Model):
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    blog = models.ForeignKey(tbl_blog, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'blog')
    def __str__(self):
        return f"{self.user.user_name} liked {self.blog.blog_title}"
    
class tbl_blog_comment(models.Model):
    user = models.ForeignKey(tbl_user, on_delete=models.CASCADE)
    blog = models.ForeignKey('tbl_blog', on_delete=models.CASCADE)
    comment = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE ,null = True, blank = True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.user_name} commented on {self.blog.blog_title}"