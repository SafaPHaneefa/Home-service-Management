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
    # Check if the user_name exists in the session
    username = request.session.get('user_name', None)  # Use get to safely access session data

    if not username:
        return redirect('login')
    print(username)  # Output the username for debugging
    return render(request, 'home.html', {'username': username})

def worker_home(request):
    username = request.session.get('user_name', 'Guest')  # Get username from session
    
    if not username:
        return redirect('login')
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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
from .models import users
import random

from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .models import users  # Make sure you import your user model
import random
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.hashers import make_password
from .models import users  # Import your User model
import random

# Function to generate a random OTP
def generate_otp():
    return random.randint(100000, 999999)

# Function to validate OTP
def validate_otp(email, otp):
    # Fetch the OTP from cache
    stored_otp = cache.get(email)  # Assume the OTP is stored with the email as the key
    return stored_otp and str(stored_otp) == str(otp)
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.core.cache import cache
from django.conf import settings
from .models import users  # Import your User model
import random

# Function to generate OTP
def generate_otp():
    return random.randint(100000, 999999)

# Function to validate OTP
def validate_otp(email, otp):
    stored_otp = cache.get(email)
    return stored_otp and stored_otp == otp

# View for registering the user
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import users  # Assuming users is the user model
 # Assuming generate_otp is a utility function to generate OTPs

def register(request):
    if request.method == 'POST':
        # Collect form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        worker_type = request.POST.get('worker')  # This needs to be used correctly

        # Initialize an errors dictionary
        errors = {}

        # Check if username exists
        if users.objects.filter(username=username).exists():
            errors['username_error'] = 'Username is already taken.'

        # Check if email exists
        if users.objects.filter(email=email).exists():
            errors['email_error'] = 'Email is already taken.'

        # If any validation errors, return with error messages
        if errors:
            for key, error in errors.items():
                messages.error(request, error)
            return render(request, 'register.html')

        # If no errors, proceed with OTP generation and registration
        try:
            # Hash the password
            hashed_password = make_password(password)

            # Create user instance
            new_user = users(username=username, email=email, password=hashed_password, role=role, work="null")
            new_user.save()

            # Generate OTP and send it to the user's email
            otp = generate_otp()
            cache.set(email, otp, timeout=300)  # Store OTP for 5 minutes

            # Store email and OTP in session for later use
            request.session['registration_email'] = email
            request.session['otp'] = otp

            # Send the OTP via email
            send_mail(
                subject='Your OTP for Registration',
                message=f'Your OTP is {otp}. Please use this to verify your account.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )

            # Notify the user and redirect to OTP verification page
            messages.success(request, "OTP has been sent to your email.")
            return redirect('verify_otp')

        except Exception as e:
            # Handle any errors that occur during user creation or OTP sending
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('register')

    return render(request, 'register.html')


# View for verifying OTP
def verify_otp_view(request):
    if request.method == 'POST':
        user_email = request.session.get('registration_email')  # Get email from session
        otp = request.POST.get('otp')
        otp_Send=request.session['otp']
        
        print(user_email)
        # Validate the OTP
        if otp:
            # OTP is valid, create user account
            # Set the user as registered in your system
            user = users.objects.get(email=user_email)  # Adjust this to your user retrieval method
            user.status = 'approved'  # or however you handle activated users
            user.save()

            # Send success email
            send_mail(
                'Registration Successful',
                'You have been successfully registered.',
                settings.DEFAULT_FROM_EMAIL,
                [user_email],
                fail_silently=False,
            )

            messages.success(request, 'You have been successfully registered!')
            return redirect('home')  # Redirect to home.html after successful verification
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    
    return render(request, 'verify_otp.html')

# View for resending OTP
def resend_otp_view(request):
    if request.method == 'POST':
        user_email = request.session.get('registration_email')  # Get email from session
        otp = generate_otp()  # Generate a new OTP
        cache.set(user_email, otp, timeout=300)  # Store OTP for 5 minutes

        # Send OTP email
        send_mail(
            subject='Your OTP for Registration',
            message=f'Your OTP is {otp}. Please use this to verify your account.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )
        
        messages.success(request, "OTP has been resent to your email.")
        return redirect('verify_otp')  # Redirect to OTP verification page

    return render(request, 'verify_otp.html')


#######################################################################




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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import users  # Import your User model



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import users
from django.contrib.auth.decorators import login_required

###########Update############

def update(request):
    username = request.session.get('user_name')

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        new_work = request.POST.get('work')

        try:
            # Fetch the user by session
            user = users.objects.get(username=username)

            # Update the user's information
            user.username = new_username
            user.email = new_email
            user.work = new_work
            user.save()

            # Update session data with new username if it changed
            request.session['user_name'] = new_username

            messages.success(request, "Profile updated successfully!")
            return redirect('view_profile')

        except users.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('home')

    else:
        # Fetch user data to prefill the form
        user = users.objects.get(username=username)
        return render(request, 'update.html', {'user': user})


#####################################################################################

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .models import users  # Import the User model

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import users  # Make sure to import your User model

def view_profile(request):
    # Check if the user is logged in by verifying the session
    username = request.session.get('user_name')
    
    if username:
        try:
            # Fetch user data from the database based on the username
            user = users.objects.get(username=username)

            # Pass the user object to the template for rendering
            return render(request, 'view_profile.html', {'user': user})

        except users.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('home')  # Redirect to home if user is not found
    else:
        messages.error(request, "You need to be logged in to view your profile.")
        return redirect('login')  # Redirect to login if not logged in
################################################

# def admin_login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
        
#         # Check against predefined credentials
#         if username == 'admin' and password == 'admin@123':
#             # Create a custom session for the admin user
#             request.session['is_admin'] = username
#             return redirect('admin_dashboard')  # Redirect to admin dashboard
#         else:
#             messages.error(request, "Invalid username or password. Please try again.")
    
#     return render(request, 'admin_login.html')


# from django.shortcuts import redirect
# from django.contrib.auth.decorators import login_required


# def admin_dashboard(request):
#     isadmin = request.session.get('is_admin', None)
#     if not isadmin :
#         return redirect('admin_login')
#     # Proceed to render the admin dashboard
#     return render(request, 'admin_dashboard.html')

#####################################################


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import users
from django.core.mail import send_mail
from django.conf import settings
import random

# Generate a random password
def generate_random_password(length=8):
    characters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.choice(characters) for _ in range(length))

def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        # Check against predefined credentials
        if username == 'admin' and password == 'admin@123':
            # Create a custom session for the admin user
            request.session['is_admin'] = True
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    
    return render(request, 'admin_login.html')


def admin_dashboard(request):
    print("hello")
    isadmin = request.session.get('is_admin', None)
    print(isadmin)
    return render(request, 'admin_dashboard.html',{'is_admin': isadmin})


def manage_users(request):
    # Fetch users where role is 'user'
    user_list = users.objects.filter(role='user')
    # Pass the data to the template
    return render(request, 'manage_users.html', {'user_list': user_list})

from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def deactivate_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        try:
            user = users.objects.get(id=user_id)
            user.delete()
            return JsonResponse({'success': True})
        except users.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})



def manage_workers(request):
    workers_list = users.objects.filter(role='worker')  # Fetch users with role as 'worker'
    return render(request, 'manage_workers.html', {'workers': workers_list})

from django.contrib.auth.hashers import make_password


@csrf_exempt
def deactivate_worker(request):
    if request.method == 'POST':
        worker_id = request.POST.get('worker_id')
        try:
            worker = users.objects.get(id=worker_id)
            worker.delete()
            return JsonResponse({'success': True})
        except users.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Worker not found.'})
    return JsonResponse({'success': False, 'message': 'Invalid request.'})

def add_worker(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        work=request.POST.get('work')
        role = 'worker'  # Setting role as worker
        password = generate_random_password()  # Generate a random password

        # Hash the password before saving it to the database
        hashed_password = make_password(password)

        # Create the worker account
        new_worker = users(
            username=username,
            email=email,
            password=hashed_password,  # Store the hashed password
            role=role,
            work=work,
        )
        new_worker.save()

        # Send approval email
        send_mail(
            subject='Welcome to Our Service!',
            message=f'Hello {username},\n\nYour account has been created successfully! Here are your login details:\nUsername: {username}\nPassword: {password}\n\nPlease change your password after logging in.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Worker added and email sent successfully!")
        return redirect('add_worker')  # Redirect to add worker page

    return render(request, 'add_worker.html')

def update_worker(request, worker_id):
    worker = users.objects.get(id=worker_id)  # Get worker by ID
    if request.method == 'POST':
        worker.username = request.POST.get('username')
        worker.email = request.POST.get('email')
        worker.save()
        messages.success(request, "Worker updated successfully!")
        return redirect('manage_workers')
    return render(request, 'update_worker.html', {'worker': worker})


def logout_view(request):
    logout(request)
    return redirect('admin_login')  # Redirect to login page after logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Bookings, users  # Import the modified Booking and User models
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Bookings, users

# Function to handle the booking form page
def booking_view(request):
    if request.method == 'POST':
        # Get data from the form
        booking_date = request.POST.get('booking_date')
        state = request.POST.get('state')
        district = request.POST.get('district')
        city = request.POST.get('city')
        street_number = request.POST.get('street_number')
        address_line = request.POST.get('address_line')
        booking_time = request.POST.get('booking_time')
        work = request.POST.get('work')  # Using 'work' as the column name
        phone_number = request.POST.get('phone_number')
        work_description = request.POST.get('work_description')

        # Print form values for debugging
        print("Form Data:", booking_date, state, district, city, street_number, booking_time, work, phone_number, work_description)

        # Validate the form fields (you can add more validations as needed)
        if not booking_date or not state or not district or not city or not street_number or not booking_time or not work or not phone_number or not work_description:
            messages.error(request, "All fields are required.")
            return redirect('booking')

        # Since there's no session, ensure you map the booking to a worker based on their role
        # Here, I'm assuming `users` table has workers
        worker = users.objects.filter(work=work, role='worker').first()  # Find the first worker of the selected type
        
        if not worker:
            messages.error(request, "No worker available for the selected type of work.")
            return redirect('booking')

        # Save booking to the database
        booking = Bookings(
            user=worker,  # Associate the booking with a worker
            booking_date=booking_date,
            state=state,
            district=district,
            city=city,
            street_number=street_number,
            address_line=address_line,
            booking_time=booking_time,
            work=work,
            phone_number=phone_number,
            work_description=work_description
        )
        booking.save()

        messages.success(request, "Your booking has been submitted successfully!")
        return redirect('booking')

    # Fetch unique worker types from the users table
    worker_types = users.objects.values_list('work', flat=True).distinct()  # Fetch distinct worker types
    return render(request, 'booking.html', {'worker_types': worker_types})

# Function to dynamically return the districts based on the selected state (AJAX)
@csrf_exempt
def get_districts(request):
    state = request.GET.get('state')
    state_districts = {
        'Kerala': ['Thiruvananthapuram', 'Ernakulam', 'Kozhikode', 'Kannur'],
        'Karnataka': ['Bangalore', 'Mysore', 'Mangalore', 'Hubli'],
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Trichy'],
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik'],
        # Add other states and their districts here
    }
    districts = state_districts.get(state, [])
    return JsonResponse({'districts': districts})

def booking(request):
    username = request.session.get('user_name', None)  # Use get to safely access session data

    if not username:
        return redirect('login')
    worker_types = users.objects.values_list('work', flat=True).distinct()
    return render(request, 'bookings.html', {'worker_types': worker_types} )

def manage_bookings(request):
    if request.session.get('is_admin'):  # Check if user is admin
        bookings = Booking.objects.all()  # Fetch all bookings from the database
        context = {
            'bookings': bookings,
            'current_year': datetime.now().year,  # Add current year for footer
        }
        return render(request, 'admin/manage_bookings.html', context)
    else:
        return redirect('admin_login')  # Redirect to login if not admin

from .models import Feedback

def submit_feedback(request):
    if request.method == "POST":
        rating = request.POST.get("rating")
        description = request.POST.get("description")
        user = request.user

        # Create Feedback entry
        Feedback.objects.create(
            rating=rating,
            description=description,
            user=user
        )
        return redirect('home')  # or any other page after feedback submission

    return render(request, 'feedback_form.html')

def search_work(request):
    # Fetch all distinct roles from the User model to populate the dropdown
    roles = User.objects.values_list('work', flat=True).distinct()

    workers = []  # Initialize an empty list for workers

    if request.method == 'POST':
        selected_role = request.POST.get('work')  # Get the selected work
        # Fetch users with the selected role
        workers = User.objects.filter(work=selected_role)

    return render(request, 'search_work.html', {'roles': roles, 'workers': workers})