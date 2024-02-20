from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
# Create your views here.


def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                messages.info(request,f"Logged in Successfully as {username}")
                return redirect('personal_expenditure')
            else:
                messages.info(request,"Account doesn't exists")
                return redirect('register')
        else:
            messages.info(request,'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password1']
        password2 = request.POST['password2']
    
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exists')
                return redirect('user_register')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Already Exists')
                return redirect('user_register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request,'Password Not The Same')
            return redirect('user_register')
    else:
        return render(request,'registration/register.html')

def logout_request(request):
    logout(request)
    messages.info(request,"Logged out successfully!")
    return redirect('/')