from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def signin(request):
    return render(request, 'app/signin.html')

def signup(request):
    return render(request, 'app/signup.html')

def login(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        
    else:
        return render(request, 'app/signin.html')

def logout(request):
    logout(request)