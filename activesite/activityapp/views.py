from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task, Profile, Team, Visit
from django.shortcuts import redirect
#from django.core.exceptions import ObjectDoesNotExist
from django.forms import modelform_factory
from .forms import TaskForm, ProfileForm, ImageUploadForm, ComleteTaskForm 
import datetime

"""def redirectToCreate():
    user = request.user
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') """


@login_required
def dashboard(request):
    role = ""
    try:
        profile=Profile.objects.get(user=request.user)
        role = profile.role
    #except ObjectDoesNotExist:
    except Profile.DoesNotExist:
        role = "" 
    user_id = request.user.id
    task = Task.objects.filter(approve=False, completed=False, selected=False)
    selected = Task.objects.filter(approve=False, completed=False, selected=True, user_id=user_id)
    #selected = Task.objects.filter(approve=False, completed=False, selected=True)
    completed = Task.objects.filter(approve=False, completed=True)
    approve = Task.objects.filter(approve=True, completed=True)
    tas = {'task':task,'completed':completed,'approve':approve, 'selected':selected, "role":role}
    return render(request, "dashboard.html", tas)



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
    
        return redirect('dashboard')  
   
    
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
        
        return redirect('dashboard')  
        
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
        
        return redirect('dashboard')  
        
    return render(request, 'create_team.html')



"""@login_required
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
        
    return render(request, 'create_profile.html')"""
@login_required
def createprofile(request):
    message=""
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.team = form.cleaned_data['team']
            profile.save()
            return redirect('dashboard')
        else:
            message='Guess you have already created a profile'
    else:
        form = ProfileForm(user=request.user)
    return render(request, 'create_profile.html', {'form': form,'message':message})




@login_required
def team_profiles(request, id):
    user = request.user
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    team = get_object_or_404(Team, id=id)
    team_name=team.name
    profiles = Profile.objects.filter(team=team)
    return render(request, 'team_profiles.html', {'profiles': profiles,'team_name':team_name})



@login_required
def monthly_team_tasks(request,teamid):
    user = request.user
    month = datetime.date.today().month
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
    return render(request, 'monthly_team_tasks.html', context)



@login_required
def select_task(request, pk):
    user = request.user
    userid = user.id
    profile = get_object_or_404(Profile, user=user)
    teamid = profile.team.id
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    task = get_object_or_404(Task, pk=pk)
    task_name = task.task
    task.team_id= teamid
    task.user_id= userid
    if request.method == 'POST':
        task.team_id= teamid
        task.user_id= userid
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)
    return render(request, 'select_task.html', {'form': form, 'task_name':task_name})


@login_required
def teams(request):
    user = request.user
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    teams = Team.objects.all()
    return render(request, 'teams.html', {'teams': teams})


@login_required
def completetask(request,id):
    data = Visit.objects.all()
    context = {
        'data' : data
    }
    return render(request,"completetask.html", context)



@login_required
def create_visit(request):
    user = request.user
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    VisitForm = modelform_factory(Visit, exclude=[])
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            visit = form.save(commit=False)
            taskid = visit.mission.id
            visit.user = request.user
            visit.save()
            return redirect('completetask', pk=taskid)
            #return redirect('visit_detail', visit.pk)
    else:
        form = ImageUploadForm()
    return render(request, 'create_visit.html', {'form': form})

@login_required
def visit_detail(request, taskid):
    task = Task.objects.get(id=taskid)
    visit = Visit.objects.filter(mission=task)
    return render(request, 'visit_detail.html', {'visit': visit})


@login_required
def complete_task(request, pk):
    user = request.user
    userid = user.id
    profile = get_object_or_404(Profile, user=user)
    teamid = profile.team.id
    try:
        Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    task = get_object_or_404(Task, pk=pk)
    visit = Visit.objects.filter(mission=task)
    task_name = task.task
    task.team_id= teamid
    task.user_id= userid
    if request.method == 'POST':
        task.team_id= teamid
        task.user_id= userid
        form = ComleteTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ComleteTaskForm(instance=task)
    return render(request, 'complete_task.html', {'form': form, 'task_name':task_name, 'visit':visit})


@login_required
def TaskDetail(request, id):
    user = request.user
    try:
        Profile.objects.get(user=user)
    #except ObjectDoesNotExist:
    except Profile.DoesNotExist:
        message="you need to create a profile first"
        return redirect('createprofile') 
    #task = Task.objects.all()
    task = get_object_or_404(Task, id=id)
    visits_count = Visit.objects.filter(mission=task).count() 
    
    return render(request, 'TaskDetail.html', {'task': task,'visits_count':visits_count})