from django.urls import path
from UWEFlixApp import views
from .models import MonthlyStatement

home_list_view = views.ViewMonthlyStatement.as_view(
    queryset=MonthlyStatement.objects.order_by("club_id")[:5],  
    context_object_name="monthly_statement_list",
    template_name="UWEFlixApp/view_monthly_statement.html",
)

urlpatterns = [
    path("", views.home, name="home"),
    path("view_monthly_statement/", home_list_view, name="view_monthly_statement"),
]