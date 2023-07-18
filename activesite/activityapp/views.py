from django.shortcuts import render, get_object_or_404

# Create your views here.
#from django.http import HttpResponse
from .models import Task, Profile, Team
from .models import Profile, Team


def index(request):
    #task = Task.objects.all()
    task = Task.objects.filter(approve=False, completed=False)
    completed = Task.objects.filter(approve=False, completed=True)
    approve = Task.objects.filter(approve=True, completed=True)
    tas = {'task':task,'completed':completed,'approve':approve}
    return render(request, "index.html", tas)
    #return HttpResponse("Hello, world. You're at the polls index.")

def dashboard(request):
    #task = Task.objects.all()
    task = Task.objects.filter(approve=False, completed=False)
    completed = Task.objects.filter(approve=False, completed=True)
    approve = Task.objects.filter(approve=True, completed=True)
    tas = {'task':task,'completed':completed,'approve':approve}
    return render(request, "account/index.html", tas)
    
def team_profiles(request, id):
    team = get_object_or_404(Team, id=id)
    profiles = Profile.objects.filter(team=team)
    return render(request, 'team_profiles.html', {'profiles': profiles})