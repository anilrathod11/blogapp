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
def archive_exp_sub_plan(request,a):
    # for i in a:
    object = Subscription.objects.get(pk=a)
    object.archive = True
    object.free_trail = False
    object.save()
    return {"message":"Archived successfully","Object_id":a}