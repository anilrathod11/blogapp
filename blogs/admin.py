from django.contrib import admin
from .models import Blog, Category,RandomPicture, StripeCustomer
# Register your models here.
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(RandomPicture)
admin.site.register(StripeCustomer)