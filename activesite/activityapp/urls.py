from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("", views.dashboard, name="dashboard"),
    path('teams/<int:id>/profiles/', views.team_profiles, name='team_profiles'),
    path('task/<int:month>/<int:teamid>/', views.monthly_team_tasks, name='monthly_team_tasks'),
    path('aprovetask/<int:id>/', views.aproveTask, name='aproveTask'),
    path('createtask', views.createTask, name='createTask'),
    path('createprofile', views.createprofile, name='createprofile'),
]