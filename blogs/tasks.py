from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

@shared_task(bind=True) 
def send_mail_func(self,mail_subject,message ,user):
    # users = get_user_model().objects.all()
    #timezone.localtime(users.date_time) + timedelta(days=2)
    # mail_subject = "Hi! Celery Testing"
    # message = "If you are liking my content, please hit the like button and do subscribe to my channel"
    # # to_email = user.email
    # to_email = ["rathodanil6512@gmail.com"]
    to_email = user
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[to_email],
        fail_silently=True,
    )
    return "Done"

@shared_task(bind=True)
def test_func (self):
    for i in range(10):
        print(i)
    return "Done"