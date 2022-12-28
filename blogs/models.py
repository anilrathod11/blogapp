from django.db import models
# from django.conf import settings
# User = settings.AUTH_USER_MODEL
from user_app.models import CustomeUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=50,default="Submitted")
    author = models.ForeignKey(CustomeUser, on_delete=models.CASCADE,related_name='user_blog')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='blog_category')
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title