from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

AUTH_PROVIDERS = {'google':'google','email':'email'}

@receiver(post_save, sender=settings.AUTH_USER_MODEL)

def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
        
class CustomeUser(AbstractUser):
    role = models.CharField(max_length=50,default='Reader')
    date_of_birth = models.DateField(null=True)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email'))
    
    def __str__(self):
        return "{}".format({"user_name":self.username,"role":self.role})

    