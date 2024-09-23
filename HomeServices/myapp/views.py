from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404 #updation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password # Make sure to import your custom user model
import random
import datetime
from django.contrib.auth.hashers import check_password #hashed password checking
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
#from .forms import CustomPasswordResetForm, CustomSetPasswordForm
# Create your views here.
def index(request):
    return render(request,'index.html')

def error(request):
    return render(request,'error.html')

def about(request):
    return render(request,'about.html')

def appointment(request):
    return render(request,'appointment.html')

def contact(request):
    return render(request,'contact.html')

def feature(request):
    return render(request,'feature.html')

def service(request):
    return render(request,'service.html')

def team(request):
    return render(request,'team.html')

def testimonial(request):
    return render(request,'testimonial.html')


def login(request):
    return render(request,'login.html')

def home(request):
    username = request.session.get('user_name', 'Guest') 
    print(username) # Get username from session or use 'Guest' as default
    return render(request, 'home.html', {'username': username})

def worker_home(request):
    username = request.session.get('user_name', 'Guest')  # Get username from session
    print(username)
    return render(request, 'worker_home.html', {'username': username})

def forgot_password(request):
    return render(request, 'custom_password_reset.html')


def userregister(request):
      # Redirect to login or another page

    return render(request, 'index.html')

def check_availability(request):
    if request.method == 'POST':
        data_type = request.POST.get('type')
        value = request.POST.get('value')
        
        if data_type == 'username':
            if User.objects.filter(username=value).exists():
                return JsonResponse({'available': False})
        elif data_type == 'email':
            if User.objects.filter(email=value).exists():
                return JsonResponse({'available': False})
        
        return JsonResponse({'available': True})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        worker_type = request.POST.get('workerType')
        # Initialize error messages
        errors = {}

        # Validate username
        if users.objects.filter(username=username).exists():
            errors['username'] = 'Username is already taken.'

        # Validate email
        if users.objects.filter(email=email).exists():
            errors['email'] = 'Email is already taken.'

        # Return errors if any
        if errors:
            return JsonResponse({'errors': errors})

        # Create user
        if role == 'user':
            worker_type = "null"
            user = users(username=username, email=email, password=make_password(password), role=role, work=worker_type)
            user.save()
        else:
            user = users(username=username, email=email, password=make_password(password), role=role, work=worker_type)
            user.save()
        if(user):
            return redirect(login)

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Find the user by email using your custom users model
            user = users.objects.get(email=email)

            # Check if the password is correct
            if check_password(password, user.password):                # Log the user in by setting session data
                request.session['user_role'] = user.role
                request.session['user_name'] = user.username
                print(request.session['user_name'])

                messages.success(request, "Login successful!")

                # Redirect based on the user's role
                if user.role == 'admin':
                    return redirect('admin_home')  # Redirect to admin home
                elif user.role == 'worker':
                    return redirect('worker_home')  # Redirect to worker's home page
                else:  # Assuming the other role is 'user'
                    return redirect('home')  # Redirect to user's home page
            else:
                messages.error(request, "Invalid email or password.")
                return redirect('login')

        except users.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()  # Clears all session data
    messages.success(request, "Logged out successfully.")
    return redirect('login')

@login_required
def update(request):
    user = request.user  # Fetch the logged-in user

    if request.method == 'POST':
        # Handle form submission to update the profile
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        role = request.POST['role']
        work = request.POST['work']

        # Save the updated data
        user.username = username
        user.email = email
        user.set_password(password)  # Remember to hash the password
        user.role = role
        user.work = work
        user.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('home')

    # Initial page load: display the current user data
    context = {
        'username': user.username,
        'email': user.email,
        'password': user.password,
        'role': user.role,
        'work': user.work,
    }
    return render(request, 'update.html', context)


def view_profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = users.objects.get(email=email)

            if check_password(password, user.password):
                request.session['user_role'] = user.role
                request.session['user_name'] = user.username

                # Print session data to check if it's being set
                print(f"User role: {request.session['user_role']}")
                print(f"User name: {request.session['user_name']}")
                print(f"Session data: {request.session.items()}")

                messages.success(request, "Login successful!")
                if user.role == 'admin':
                    return redirect('admin_home')
                elif user.role == 'worker':
                    return redirect('worker_home')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid email or password.")
                return redirect('login')

        except users.DoesNotExist:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'login.html')
