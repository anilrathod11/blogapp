from rest_framework import serializers
from sub_plan_app.models import SubPlan,Subscription

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubPlan
        fields = "__all__"
        
class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"