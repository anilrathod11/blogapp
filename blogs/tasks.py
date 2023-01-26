from django.contrib.auth import get_user_model

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from sub_plan_app.models import Subscription
import datetime
from datetime import date
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
from sub_plan_app.api.serializers import SubscriptionSerializer


@shared_task(bind=True) 
def send_mail_func(self):
    # users = get_user_model().objects.all()
    #timezone.localtime(users.date_time) + timedelta(days=2)
    mail_subject = "Hi! Celery Testing"
    message = "Testing celery beat in django"
    # # to_email = user.email
    to_email = ["rathodanil6512@gmail.com"]
    # to_email = user
    send_mail(
        subject = mail_subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        # recipient_list=[to_email],
        recipient_list=to_email,
        fail_silently=True,
    )
    return "Done"

@shared_task(bind=True)
def test_func (self):
    for i in range(10):
        print(i)
    return "Done"
        
@shared_task(bind=True)
def archive_sub(request,a):
    object = Subscription.objects.get(pk=a)
    object.archive = True
    object.save()
    return {"message":"Archived successfully","Object_id":a}

@shared_task(bind=True)
def schedule_exp_sub(request):
    sub = Subscription.objects.filter(exp_date__date = date.today())
    count1 = sub.count()
    serializer = SubscriptionSerializer(sub,many=True)
    for object in sub:
        hour1 = object.exp_date.hour
        minute1 = object.exp_date.minute
        schedule, created = CrontabSchedule.objects.get_or_create(hour = hour1, minute = minute1)
        task = PeriodicTask.objects.create(crontab = schedule, name="schedule_archive_task_{}".format(object.id), task='sub_plan_app.tasks.archive_exp_sub_plan', args = [object.id,object.id])#, args = json.dumps([[2,3]]))
    return {"messege":"All workers are set according to exp datetime","count":count1,"date":date.today()}