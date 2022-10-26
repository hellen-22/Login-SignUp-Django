from django.shortcuts import render
import requests

# Create your views here.
def signup(request):
    return render(request, 'account/signup.html')

def login(request):
    return render(request, 'account/login.html')

def users(request):
    response = requests.get('http://127.0.0.1:8000/auth/users/')
    users = response.json()

    return render(request, 'account.html', {'users': users})