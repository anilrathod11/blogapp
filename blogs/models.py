from django.db import models
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
    reviewer = models.ForeignKey(CustomeUser,on_delete=models.CASCADE,related_name='blog_to_review',null=True)
    public = models.BooleanField(default=False)
    archive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class CommentOnBlog(models.Model):
    comment = models.CharField(max_length=200)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_comments')
    commented_by = models.ForeignKey(CustomeUser,on_delete=models.CASCADE,related_name='user_comment')
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.commented_by
    
class ContentWriterPerformance(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_performance')
    status = models.CharField(max_length=50)
    reason = models.CharField(max_length=250)
    reviewer = models.ForeignKey(CustomeUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.reviewer
    
    
class RandomPicture(models.Model):
    user = models.ForeignKey(CustomeUser, on_delete=models.CASCADE,related_name='user_image')
    rand_pic = models.ImageField(upload_to="image",blank=True)
    
    def __str__(self):
        return self.user.username

class StripeCustomer(models.Model):
    user = models.OneToOneField(to=CustomeUser, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username