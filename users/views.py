from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

def login_user(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user=authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.warning(request, 'something went wrong')
            return redirect('login')
    else:
        return render(request, 'users/login.html' )

def logout_user(request):
    logout(request)
    messages.info(request, 'Your session has ended. Please, log in to continue')
    return redirect('login')
