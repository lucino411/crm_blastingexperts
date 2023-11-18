from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# from .models import Lead


@login_required
def dashboard(request):
    return render(request, 'dashboard/dashboard_home.html')

def login_user(request):
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authentication
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You Have been logged In')
            return redirect('dashboard_home')
        else:
            messages.warning(
                request, 'There was and Error Loggin In, Plesae try again')
            return redirect('login_home')
    else:
        return render(request, 'dashboard/login_home.html')

@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login_home')


def page_not_found404(request, exception):    
    return render(request, 'dashboard/404.html')
