from django.shortcuts import render,redirect
from .forms import RegistrationForm,LoginForm
from .models import Account
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate ,login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            email=form.cleaned_data['email']
            phone_no=form.cleaned_data['phone_no']
            password=form.cleaned_data['password']
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,password=password,username=username)
            user.phone_no=phone_no
            user.save()
            subject="Registration Successfull"
            message="Welcome to our Website ,You account is created"
            email_from=settings.EMAIL_HOST_USER
            recipient_list=[user.email]
            print(recipient_list)
            try:
                send_mail(subject,message,email_from,recipient_list)
                messages.success(request,"Registration done successfully")
                form=RegistrationForm()
            except Exception as e:
                print(e)
                messages.success(request,"Registration done successfully")
                form=RegistrationForm()
    else:
        form=RegistrationForm()
    context={
        'form':form
    }
    return render(request, 'core/signup.html',context)

def login(request):
    form=LoginForm(request.POST)
    if form.is_valid():
        email=form.cleaned_data['email']
        password=form.cleaned_data['password']
        user=authenticate(request,email=email,password=password)
        print("user is",user)
        if user is not None:
            auth_login(request,user)
            messages.success(request,"Welcome to Dashboard")
            return redirect('dashboard')
        else:
            messages.error(request,"Your email or password is incorrect")
    form=LoginForm()
    return render(request,'core/login.html',{'form':form})

def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user=request.user
    context={
        'user':user
    }
    return render(request,'users/dashboard.html',context)