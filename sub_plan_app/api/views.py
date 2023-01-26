from django.template.loader import get_template
from user_app.models import CustomeUser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from rest_framework.response import Response
from sub_plan_app.models import SubPlan,Subscription
from sub_plan_app.api.serializers import PlanSerializer,SubscriptionSerializer
from rest_framework import status
import stripe
from dateutil.relativedelta import relativedelta
from rest_framework.decorators import api_view,permission_classes
from datetime import date
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from datetime import datetime
import pytz
from datetime import datetime, timedelta
import json

from django.shortcuts import render,redirect
IST = pytz.timezone('Asia/Kolkata')

class PlanAV(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        plans = SubPlan.objects.all()
        serializer = PlanSerializer(plans,many=True)
        return Response({"list_of_subscription_plan":serializer.data},status=status.HTTP_200_OK)
    
    # permission_classes = [IsAdminUser]
    def post(self, request):
        user = CustomeUser.objects.get(pk=request.user.id)
        if user.role == "Admin":
            serializer = PlanSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"Plan object created successfully","created_object":serializer.data},status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors)
        else:
            return Response({'message':"Only admin can post plan"},status=status.HTTP_400_BAD_REQUEST)
        
def pay_success(request):
    session = stripe.checkout.Session.retrieve(request.GET['session_id'])
    # print(session)
    plan_id=session.client_reference_id
    plan=SubPlan.objects.get(pk=plan_id)
    # user=request.user

    if plan.title == "Monthly":
        exp_date = datetime.now(IST) + timedelta(minutes = 2)
        # + relativedelta(months = 1)
    elif plan.title == "Quarterly":
        exp_date = datetime.now(IST)
        # + relativedelta(months = 3)     
    elif plan.title == "Half Year":
        exp_date = datetime.now(IST)
        # + relativedelta(months = 6) 
    else:
        exp_date = datetime.now(IST)
        # + relativedelta(months = 12)           
    user = CustomeUser.objects.get(email=session.customer_details["email"])
    sub_plan =  Subscription.objects.create(
    	            plan=plan,
    	            user=user,
    	            price=plan.pricing,
                    exp_date = exp_date
                )
    sub_plan.save()
    # exp_date = exp_date + timedelta(minutes = 2)
    hour1 = exp_date.hour
    minute1 = exp_date.minute
    print(hour1,minute1)
    schedule, created = CrontabSchedule.objects.get_or_create(hour = hour1, minute = minute1)
    task = PeriodicTask.objects.create(crontab = schedule, name="schedule_archive_task_{}".format(sub_plan.id), task='sub_plan_app.tasks.archive_exp_sub_plan',args = json.dumps([sub_plan.id]))
    return render(request, 'success.html')

# Cancel
def pay_cancel(request):
	return render(request, 'cancel.html')

        
stripe.api_key='sk_test_51MPQOQSEibFHYgaHJ5sq1lfdCzuaCIfBdnTndNQGeqbMDPWNsu1BsrVXlL6snHilMRYikF7auakNwt55doXWocXv00HhTqoMvM'
def checkout_session(request,plan_id):
    plan=SubPlan.objects.get(pk=plan_id)
    session=stripe.checkout.Session.create(
    	payment_method_types=['card'],
    	line_items=[{
          'price_data': {
            'currency': 'inr',
            'product_data': {
              'name': plan.title,
            },
            'unit_amount': plan.pricing*100
          },
          'quantity': 1,
        }],
        mode='payment', 
        success_url='http://127.0.0.1:8000/sub/pay_success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='http://127.0.0.1:8000/sub/pay_cancel',
        client_reference_id=plan_id
    )
    return redirect(session.url, code=303)

@api_view(['DELETE',])
def archive_sub_plan(request):
    archive_subcription = Subscription.objects.all().exclude(archive=True)
    for object in archive_subcription:
        if object.exp_date <= datetime.datetime.now():
            object.archive = True
            print("anil")
            object.save()
    return Response({"message":"Archived successfully"},status=status.HTTP_200_OK)

@api_view(["POST",])
@permission_classes([IsAuthenticated])
def add_free_trail(request,pk):
    if request.method == "POST":
        try:
            sub_plan = SubPlan.objects.get(pk=pk)
        except SubPlan.DoesNotExist():
            return Response({'message':"Plan does not exit"}, status=status.HTTP_404_NOT_FOUND)
        exp_date = datetime.now(IST) + timedelta(days=sub_plan.validity_days)
        subscription =  Subscription.objects.create(
    	        plan=sub_plan,
    	        user=request.user,
    	        price=sub_plan.pricing,
                exp_date = exp_date,
                free_trail = True
            )
        subscription.save()
        hour1 = exp_date.hour
        minute1 = exp_date.minute
        print(hour1,minute1)
        schedule, created = CrontabSchedule.objects.get_or_create(hour = hour1, minute = minute1)
        task = PeriodicTask.objects.create(crontab = schedule, name="schedule_archive_task_{}".format(subscription.id), task='sub_plan_app.tasks.archive_exp_sub_plan',args = json.dumps([subscription.id]))
        serializer = SubscriptionSerializer(subscription)
        return Response({"message":"Free trail created successfully","created_object":serializer.data},status=status.HTTP_201_CREATED)