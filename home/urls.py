from django.urls import path
from . import views
from .views import (
    GoalListView,
    GoalDetailView,
    GoalDeleteView,
    GoalUpdateView,
    
)


urlpatterns = [
    path('', views.home , name='homepage'),
    path('timetrends/', views.time_trends , name='timetrends'),
    path('acttrends/', views.act_trends , name='acttrends'),
    path('activities/register', views.registeractivities, name='registeractivity'),
    path('goals/<int:pk>/', GoalDetailView.as_view(), name='goal-detail'),
    path('goals/<int:pk>/update/', GoalUpdateView.as_view(), name='goal-update'),
    path('goals/<int:pk>/delete/', GoalDeleteView.as_view(), name='goal-delete'),
    path('goals/register', views.registergoals, name='registergoal'),
    path('goals/view', GoalListView.as_view(), name='viewgoal'),
    path('activities/log', views.logactivities, name='activity-log'),
    
        
]