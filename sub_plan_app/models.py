from django.db import models
from user_app.models import CustomeUser


class SubPlan(models.Model):
    # user = models.OneToOneField(to=CustomeUser, on_delete=models.CASCADE,related_name="user_plan")
    title = models.CharField(max_length=150)
    pricing = models.IntegerField()
    validity_days = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title
    
class Subscription(models.Model):
    user=models.ForeignKey(CustomeUser, on_delete=models.CASCADE,null=True)
    plan=models.ForeignKey(SubPlan, on_delete=models.CASCADE,null=True)
    price=models.CharField(max_length=50)
    reg_date=models.DateTimeField(auto_now_add=True,null=True)
    exp_date = models.DateTimeField(null=True)
    archive = models.BooleanField(default=False)
    free_trail = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.user.username