from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Profile, Team, Visit
from django.shortcuts import redirect
#from django.core.exceptions import ObjectDoesNotExist
from .forms import TaskForm

"""def redirectToCreate():
    user = request.user
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') """


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
    user_id = request.user.id
    task = Task.objects.filter(approve=False, completed=False, selected=False)
    selected = Task.objects.filter(approve=False, completed=False, selected=True, user_id=user_id)
    completed = Task.objects.filter(approve=False, completed=True)
    approve = Task.objects.filter(approve=True, completed=True)
    tas = {'task':task,'completed':completed,'approve':approve, 'selected':selected}
    return render(request, "account/index.html", tas)



@login_required
def aproveTask(request, id):
    user = request.user
    try:
        Profile.objects.get(user=user)
    #except ObjectDoesNotExist:
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    #task = Task.objects.all()
    tasks = get_object_or_404(Task, id=id)
    visits = Visit.objects.filter(mission=tasks)
    if request.method == 'POST':
        approve = request.POST.get('approve')        
        if approve == 'true':
            tasks.approve = True
        else: 
            tasks.approve = False 
        tasks.save()
    
        return redirect('home')  
   
    
    return render(request, 'approve.html', {'tasks': tasks,'visits':visits})



@login_required
def createTask(request):
    user = request.user
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    if request.method == 'POST':
        task = request.POST['task']
        description = request.POST['description']
        region = request.POST['region']
        area = request.POST['area']
        
        new_task = Task.objects.create(
            task=task,
            description=description,
            region=region, 
            area=area
        )
        new_task.save()
        
        return redirect('home')  
        
    return render(request, 'create_task.html')



@login_required
def createTeam(request):
    user = request.user
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    if request.method == 'POST':
        name = request.POST['name']
        
        new_team = Team.objects.create(
            name=name,
        )
        new_team.save()
        
        return redirect('home')  
        
    return render(request, 'create_task.html')



@login_required
def createprofile(request):
    if request.method == 'POST':
        user = request.user
        team = get_object_or_404(Team, id=user.id)
        role = request.POST['role']
        region = request.POST['region']
        country = request.POST['country']
        area = request.POST['area']
        
        new_profile = Profile.objects.create(
            user=user,
            team = team,
            role=role,
            region=region, 
            country = country,
            area=area
        )
        new_profile.save()
        
        return redirect('home')  
        
    return render(request, 'create_profile.html')




@login_required
def team_profiles(request, id):
    user = request.user
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    team = get_object_or_404(Team, id=id)
    profiles = Profile.objects.filter(team=team)
    return render(request, 'team_profiles.html', {'profiles': profiles})



@login_required
def monthly_team_tasks(request, month, teamid):
    user = request.user
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    team = get_object_or_404(Team, pk=teamid)
    tasks = Task.objects.filter(
    completed=True,
    updated_at__month=month,
    team_id=teamid
    )
    visits = Visit.objects.filter(updated_at__month=month,mission=tasks)
    context = {
    'team': team,
    'tasks': tasks,
    'month': month,
    'visits':visits
    }
    return render(request, 'tasks.html', context)



@login_required
def select_task(request, pk):
    user = request.user
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task.description = form.cleaned_data['description']    
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
        
    return render(request, 'select_task.html', {'form': form})