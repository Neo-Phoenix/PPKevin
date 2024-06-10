from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from app.models import *
from app.forms import *

# Create your views here.


def signin(request):
    return render(request, 'app/signin.html')

def signup(request):
    return render(request, 'app/signup.html')

def overview(request):
    return render(request, 'app/overview.html')

def event_manager(request):
    events = Event.objects.all()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_manager')
    else:
        form = EventForm()
    return render(request, 'app/event_manager.html', {'form': form, 'events': events})

def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_manager')
    else:
        form = EventForm(instance=event)
    return render(request, 'event_form.html', {'form': form})

def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('app/event_manager')
    return render(request, 'event_confirm_delete.html', {'event': event})

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'event_manager/event_form.html', {'form': form})

def login(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request, username=username, password=password)
    if user is not None:
        django_login(request, user)
        return redirect('overview')
    else:
        messages.warning(request, 'Wrong credentials.')
        return render(request, 'app/signin.html', {'username' : username})

def register(request):
    #POST is een dictionary object, POST.get(key, default=None) is hetzelfda als QueryDict.get(key, default=None)
    firstname = request.POST.get("firstname")
    lastname = request.POST.get("lastname")
    password = request.POST.get("password")
    email = request.POST.get("email")
    passwordCheck = request.POST.get("passwordCheck")

    #Check of alle values ingevuld zijn met all() dit filtered ook None values eruit van QueryDict.get(key, default=None) anders error message
    if not all([firstname, lastname, email, password, passwordCheck]):
        messages.warning(request, 'Error missing fields.')
        return render(request, 'app/signup.html', {'firstname': firstname, 'lastname': lastname, 'email': email})
    
    #Email validatie met Django email validator
    try:
        validate_email(email)
        #Validate_email van validators gooit een error, geen boolean, dus error handling moet gebeuren
    except ValidationError:
        messages.warning(request, 'Invalid email address.')
        return render(request, 'app/signup.html', {'firstname': firstname, 'lastname': lastname, 'email': email})

    #Check paswoord ook hetzelfde is
    if password == passwordCheck:
        User.objects.create_user(username=email, email=email, password=password, first_name=firstname, last_name=lastname)
        messages.warning(request, "Succesfully registered, please login.")
        return render(request, 'app/signin.html', {'firstname': firstname, 'lastname': lastname, 'email': email})
    else:
        messages.warning(request, "Password doesn't match.")
        return render(request, 'app/signup.html', {'firstname': firstname, 'lastname': lastname, 'email': email})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('signin')
