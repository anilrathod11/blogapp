from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
class CustomeUser(AbstractUser):
    role = models.CharField(max_length=50,default='Reader')
    date_of_birth = models.DateField(null=True)
    
    def __str__(self):
        return self.username

# class CustomeUser(AbstractBaseUser):
#     email = models.EmailField(verbose_name = "email_address",max_length=200,unique=True)
#     role = models.CharField(max_length=50,default="Reader")
#     date_of_birth = models.DateField()
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
    
#     objects = MyUserManager()
    