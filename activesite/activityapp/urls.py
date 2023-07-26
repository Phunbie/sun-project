from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("", views.dashboard, name="dashboard"),
    path('teams/<int:id>/profiles/', views.team_profiles, name='team_profiles'),
    path('task/<int:teamid>/', views.monthly_team_tasks, name='monthly_team_tasks'),
    path('aprovetask/<int:id>/', views.aproveTask, name='aproveTask'),
    path('createtask', views.createTask, name='createTask'),
    path('createprofile', views.createprofile, name='createprofile'),
    path('createteam', views.createTeam, name='createteam'),
    path('teamprofiles/<int:id>/', views.team_profiles, name='teamprofiles'),
    path('teams', views.teams, name='teams'),
    path('selecttask/<int:pk>/', views.select_task, name='selecttask'),
    path('createvisit', views.create_visit, name='createvisit'),
    path('visitdetail/<int:taskid>/', views.visit_detail, name='visitdetail'),
    path('completetask/<int:pk>/', views.complete_task, name='completetask'),
    path('taskdetail/<int:id>/', views.TaskDetail, name='taskdetail'),
]