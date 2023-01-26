from django.urls import path,include
from sub_plan_app.api.views import PlanAV
from sub_plan_app.api import views
urlpatterns = [
    path("plan/list/",PlanAV.as_view(),name="Plan-list"),
	path('checkout_session/<int:plan_id>',views.checkout_session,name='checkout_session'),
	path('pay_success',views.pay_success,name='pay_success'),
	path('pay_cancel',views.pay_cancel,name='pay_cancel'),
    path("archive/exp/sub",views.archive_sub_plan, name="Archived Successfully"),
    path("add/free-trail/<int:pk>/",views.add_free_trail,name="Free trail"),
]