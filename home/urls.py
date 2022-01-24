from django.urls import path
from . import views
from .views import (
    GoalListView,
   
    GoalDeleteView,
    GoalUpdateView,
    
)


urlpatterns = [
    path('', views.home , name='homepage'),
    path('timetrends/daily', views.timewise_trends_daily , name='timetrends-daily'),
    path('timetrends/weekly', views.timewise_trends_weekly , name='timetrends-weekly'),
    path('timetrends/monthly', views.timewise_trends_monthly , name='timetrends-monthly'),
    path('acttrends/daily', views.act_trends_daily , name='acttrends-daily'),
    path('acttrends/weekly', views.act_trends_weekly , name='acttrends-weekly'),
    path('acttrends/monthly', views.act_trends_monthly , name='acttrends-monthly'),
    path('activities/register', views.registeractivities, name='registeractivity'),
    
    path('goals/<int:pk>/update/', GoalUpdateView.as_view(), name='goal-update'),
    path('goals/<int:pk>/delete/', GoalDeleteView.as_view(), name='goal-delete'),
    path('goals/register', views.registergoals, name='registergoal'),
    path('goals/view', GoalListView.as_view(), name='goal-list'),
    path('activities/log', views.logactivities, name='activity-log'),
    path('activities/delete', views.delete_act, name='activity-delete'),
    
    
        
]