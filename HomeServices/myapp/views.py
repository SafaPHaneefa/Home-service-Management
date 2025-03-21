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
from django.urls import reverse
from django.conf import settings
import os

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
    Services = Service_Details.objects.all()
    return render(request,'service.html',{'Service_Details':Services})

def team(request):
    return render(request,'team.html')

def testimonial(request):
    return render(request,'testimonial.html')


def login(request):
    return render(request,'login.html')
from django.utils import timezone

def home(request):
    # Check if the user_name exists in the session
    username = request.session.get('user_name', None)  # Use get to safely access session data

    if not username:
        return redirect('login')
    print(username)
    active_announcements = Announcement.objects.filter(expires_at__gt=timezone.now()).order_by('-created_at')
    Services = Service_Details.objects.all()
      # Output the username for debugging
    return render(request, 'home.html', {'username': username,'active_announcements': active_announcements,'Service_Details':Services})
    

def worker_home(request):
    username = request.session.get('user_name', 'Guest')
    user_id=request.session.get('user_id')  # Get username from session
    
    if not username:
        return redirect('login')
    print(username)
    return render(request, 'worker_home.html', {'username': username,'user_id':user_id})

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
            new_user = users(username=username, email=email, password=hashed_password, role="user")
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

##---Worker registration---##
from django.shortcuts import render, redirect
# from .models import Workers, Services
from django.contrib import messages
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from datetime import datetime
from .models import Workers_Details, Service_Details

def worker_registration(request):
    services = Service_Details.objects.all()  # Fetch services from the Service model
    error_messages = {}  # Dictionary to hold error messages

    if request.method == 'POST':
        # Get form data
        worker_name = request.POST.get('worker_name')
        profile_image = request.FILES.get('profile_image')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        state = request.POST.get('state')  # Capture state
        district = request.POST.get('district')  # Capture district
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        phone_no = request.POST.get('phone_no')
        experience = request.POST.get('experience')
        certificate = request.FILES.get('certificate')
        services_selected = request.POST.getlist('services')
        resume = request.FILES.get('resume')

        # Validate file types
        if profile_image and not profile_image.name.endswith(('.png', '.jpg', '.jpeg')):
            error_messages['profile_image'] = "Profile image must be a PNG or JPG file."

        if certificate and not certificate.name.endswith('.pdf'):
            error_messages['certificate'] = "Certificate must be a PDF file."

        if resume and not resume.name.endswith('.pdf'):
            error_messages['resume'] = "Resume must be a PDF file."

        # Email validation (check if it exists or is invalid)
        if Workers_Details.objects.filter(email=email).exists():
            error_messages['email'] = "Email already exists!"

        # Additional validations...
        try:
            validate_email(email)  # Check if the email is in the correct format
        except ValidationError:
            error_messages['email'] = "Invalid email format!"

        if len(phone_no) != 10 or not phone_no.isdigit():
            error_messages['phone_no'] = "Phone number must be 10 digits!"

        dob_datetime = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - dob_datetime.year - ((today.month, today.day) < (dob_datetime.month, dob_datetime.day))
        if age < 18:
            error_messages['age'] = "You must be at least 18 years old to register!"

        # If there are any error messages, render the form again with errors
        if error_messages:
            return render(request, 'worker_registration.html', {'services': services, 'error_messages': error_messages})

        # Create the worker instance with state and district
        worker = Workers_Details(
            worker_name=worker_name,
            profile_image=profile_image,
            email=email,
            gender=gender,
            dob=dob,
            state=state,  # Store state
            district=district,  # Store district
            address=address,
            pincode=pincode,
            phone_no=phone_no,
            experience=experience,
            certificate=certificate,
            services=", ".join(services_selected),  # Save selected services as a comma-separated string
            resume=resume
        )
        worker.save()

        # Send a confirmation email after successful registration
        send_mail(
            subject='Registration Successful',
            message='Your registration is successful. Wait for admin approval.',
            from_email='safaphaneefa@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect('worker_registration_success')

    return render(request, 'worker_registration.html', {'services': services})

def registration_success(request):
    return render(request, 'registration_success.html')


# View for verifying OTP
def verify_otp_view(request):
    if request.method == 'POST':
        user_email = request.session.get('registration_email')  # Get email from session
        # otp = request.POST.get('otp')
        # otp_Send=request.session['otp']
        
        # print(user_email)
        # # Validate the OTP
        # if otp:
        #     # OTP is valid, create user account
        #     # Set the user as registered in your system
        #     user = users.objects.get(email=user_email)  # Adjust this to your user retrieval method
        #     user.status = 'approved'  # or however you handle activated users
        #     user.save()

            # messages.success(request, 'You have been successfully registered!')
        return redirect('home')  # Redirect to home.html after successful verification
        # else:
        #     messages.error(request, 'Invalid OTP. Please try again.')
    
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

def worker_bookings(request):
    user_id = request.session.get('worker_id')  # Get the logged-in user's ID
    print("Worker_id",user_id)
    bookings = Bookings.objects.filter(worker_id=user_id)  # Fetch bookings related to the logged-in worker

    context = {
        'bookings': bookings
    }
    return render(request, 'worker_bookings.html', context)




import string
from .models import Workers_Details, users

def approve_worker(request):
    if request.method == 'POST':
        worker_id = request.POST.get('worker_id')
        worker = Workers_Details.objects.get(id=worker_id)
        worker.is_active = True
        worker.save()
        
        # Auto-generate password
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # Send email
        send_mail(
            'Your Account Has Been Approved',
            f'Hello {worker.worker_name},\n\nYour account has been approved. Your password is: {password}\n\nPlease change your password after logging in.',
            'safaphaneefa@gmail.com',  # Replace with your email
            [worker.email],  # Recipient email
            fail_silently=False,
        )
        hashed_password = make_password(password)

        # Save to Users table
        users.objects.create(
            username=worker.worker_name,
            email=worker.email,
            worker_id=worker.id,
            role="worker",
            password=hashed_password  # You might want to hash the password
        )

        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'message': 'Invalid request method.'})

#######################################################################




def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check for admin login
        if username == 'admin' and password == 'admin@123':
            request.session['is_admin'] = True
            request.session['user_name'] = 'Admin'
            messages.success(request, "Admin login successful!")
            return redirect('admin_dashboard')

        # Regular user login
        try:
            user = users.objects.get(Q(email=username) | Q(username=username))
            if check_password(password, user.password):
                request.session['user_role'] = user.role
                request.session['user_name'] = user.username
                request.session['user_id'] = user.id
                messages.success(request, "Login successful!")
                if user.role == 'worker':
                    request.session['worker_id']=user.worker_id
                    return redirect('worker_home')
                else:
                    return redirect('home')
            else:
                messages.error(request, "Invalid username/email or password.")
        except users.DoesNotExist:
            messages.error(request, "Invalid username/email or password.")

    return render(request, 'login.html')

def logout(request):
    request.session.flush()  # Clears all session data
    messages.success(request, "Logged out successfully.")
    return redirect('index')

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
            worker_id = user.worker_id
            
            # Check if worker_id is "none" (as a string)
            if worker_id == "none":
                # Render the view_profile.html with user data only
                return render(request, 'view_profile.html', {'user': user, 'work': user})  # Send None for work
            
            # If worker_id is valid, fetch the worker details
            work = Workers_Details.objects.get(id=worker_id)

            # Pass the user object and work object to the template for rendering
            return render(request, 'view_profile.html', {'user': user, 'work': work})

        except users.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('home')  # Redirect to home if user is not found
    else:
        messages.error(request, "You need to be logged in to view your profile.")
        return redirect('login')  # Redirect to login if not logged in
################################################


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
    
    return render(request, 'login.html')
from django.db.models import Count

def admin_dashboard(request):
    total_users = users.objects.count()
    total_workers = Workers_Details.objects.count()
    total_bookings = Bookings.objects.count()
    total_services = Service_Details.objects.count()

    # Get bookings by district in Kerala
    kerala_districts = [
        'Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 
        'Kollam', 'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 
        'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad'
    ]

    bookings_by_district = (
        Bookings.objects.filter(state='Kerala')
        .values('district')
        .annotate(count=Count('id'))
    )

    district_counts = {district: 0 for district in kerala_districts}
    for booking in bookings_by_district:
        district_counts[booking['district']] = booking['count']

    # Prepare data for the chart
    districts = list(district_counts.keys())
    counts = list(district_counts.values())

    # Get count of registered workers based on services
    services = Service_Details.objects.all()
    service_counts = {service.service_name: Workers_Details.objects.filter(services__icontains=service.service_name).count() for service in services}

    # Prepare data for the chart
    service_names = list(service_counts.keys())
    worker_counts = list(service_counts.values())

    context = {
        'total_users': total_users,
        'total_workers': total_workers,
        'total_bookings': total_bookings,
        'total_services': total_services,
        'districts': districts,
        'district_counts': counts,
        'service_names': service_names,
        'worker_counts': worker_counts,
    }

    return render(request, 'admin_dashboard.html', context)

import re
from pdfminer.high_level import extract_text

def extract_details_from_pdf(file_path):
    """Extract text from PDF and search for specific patterns."""
    text = extract_text(file_path)  # Extract text from the uploaded PDF
    details = {}

    # Regex patterns for required fields
    patterns = {
        "name": r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)",  # Match names like "SABAHAMOL P HANEEFA"
        "email": r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        "phone": r"\+?\d{10,15}",  # Match phone numbers
        "qualification": r"(Bachelor|Master|MCA|BCA|Higher Secondary Education).*",
        "skills": r"(Technical Skills|Skills|Skills:)\s*([A-Za-z, ]+)",  # Match skills
        "experience": r"(Experience|Projects|Internship).*",
        "linkedin": r"(https?://(www\.)?linkedin\.com/in/[a-zA-Z0-9-]+)"  # Match LinkedIn URL
    }

    # Extract and store matched fields
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # For skills, we want the second capturing group
            details[key] = match.group(2) if key == "skills" else match.group(0)
        else:
            details[key] = "Not Found"

    return details
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def upload_resume(request):
    if not request.session.get('is_admin'):
        return redirect('login')
    details = {}
    if request.method == "POST" and request.FILES.get("resume"):
        uploaded_file = request.FILES["resume"]
        fs = FileSystemStorage()
        file_path = fs.save(uploaded_file.name, uploaded_file)  # Save file in media directory
        file_path = fs.path(file_path)  # Get file path for processing
        
        # Extract details from the uploaded file
        details = extract_details_from_pdf(file_path)

    return render(request, "upload_resume.html", {"details": details})





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
    workers = Workers_Details.objects.all()  # Fetch all workers from the workers_details table
    return render(request, 'manage_workers.html', {'workers': workers})
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

from django.shortcuts import render
from .models import Workers_Details

def add_worker(request, worker_id):
    worker = None
    password = None

    # Fetch worker details using worker_id from the URL
    try:
        worker = Workers_Details.objects.get(id=worker_id)
    except Workers_Details.DoesNotExist:
        worker = None

    # The password can be regenerated or passed along as needed (if stored or sent in the approval)
    # password = 'Generate or retrieve if required'

    return render(request, 'add_worker.html', {'worker': worker, 'password': password})



def update_worker(request):
    user_id=request.session.get('user_id')
    worker = users.objects.get(id=user_id)  # Get worker by ID
    if request.method == 'POST':
        worker.username = request.POST.get('username')
        worker.email = request.POST.get('email')
        worker.save()
        messages.success(request, "Worker updated successfully!")
        return redirect('manage_workers')
    return render(request, 'update_worker.html', {'worker': worker})


def logout_view(request):
    logout(request)
    return redirect('index')
  # Redirect to login page after logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Bookings, users  # Import the modified Booking and User models
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Bookings, users

# Function to handle the booking form page
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Bookings, users, Workers_Details

def booking_view(request):
    if request.method == "POST":
        try:
            # Get form data
            user_id = request.session.get('user_id')
            worker_id = request.POST.get('selected_worker')
            booking_date = request.POST.get('booking_date')
            booking_time = request.POST.get('booking_time')
            state = request.POST.get('state')
            district = request.POST.get('district')
            city = request.POST.get('city')
            street_number = request.POST.get('street_number')
            address_line = request.POST.get('address_line')
            work = request.POST.get('work')
            phone_number = request.POST.get('phone_number')
            work_description = request.POST.get('work_description')

            # Validate required fields
            if not all([user_id, worker_id, booking_date, booking_time, state, 
                       district, city, street_number, address_line, work, 
                       phone_number, work_description]):
                return JsonResponse({
                    'success': False,
                    'message': 'All fields are required.'
                })

            # Get worker and validate availability
            worker = Workers_Details.objects.get(id=worker_id)
            existing_booking = Bookings.objects.filter(
                worker=worker,
                booking_date=booking_date
            ).exists()

            if existing_booking:
                return JsonResponse({
                    'success': False,
                    'message': 'Selected worker is no longer available for this date.'
                })

            # Create booking
            booking = Bookings.objects.create(
                user_id=user_id,
                worker=worker,
                booking_date=booking_date,
                booking_time=booking_time,
                state=state,
                district=district,
                city=city,
                street_number=street_number,
                address_line=address_line,
                work=work,
                phone_number=phone_number,
                work_description=work_description
            )

            # Update worker status
            worker.status = "Booked"
            worker.save()

            return JsonResponse({
                'success': True,
                'message': 'Booking successful!'
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Booking failed: {str(e)}'
            })

    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

# Function to dynamically return the districts based on the selected state (AJAX)
@csrf_exempt
def get_districts(request):
    state = request.GET.get('state')
    state_districts = {
       'Kerala': [
            'Alappuzha', 'Ernakulam', 'Idukki', 'Kannur', 'Kasaragod', 
            'Kollam', 'Kottayam', 'Kozhikode', 'Malappuram', 'Palakkad', 
            'Pathanamthitta', 'Thiruvananthapuram', 'Thrissur', 'Wayanad'
        ],
        'Karnataka': ['Bangalore', 'Mysore', 'Mangalore', 'Hubli'],
        'Tamil Nadu': ['Chennai', 'Coimbatore', 'Madurai', 'Trichy'],
        'Maharashtra': ['Mumbai', 'Pune', 'Nagpur', 'Nashik'],
        # Add other states and their districts here
    }
    districts = state_districts.get(state, [])
    return JsonResponse({'districts': districts})

# def booking(request):
#     username = request.session.get('user_name', None)  # Use get to safely access session data

#     if not username:
#         return redirect('login')
#     worker_types = Service_Details.objects.values_list('service_name', flat=True).distinct()
    # return render(request, 'bookings.html', {'worker_types': worker_types} )

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Q
from .models import Workers_Details, Bookings
from datetime import datetime

def booking(request):
    if request.method == "POST" and request.POST.get('update_workers') == 'true':
        # Get form data
        booking_date = request.POST.get('booking_date')
        state = request.POST.get('state')
        district = request.POST.get('district')
        work_type = request.POST.get('work')

        # Base query for workers
        available_workers = Workers_Details.objects.filter(
            is_active=True,
            status="Available"
        )

        # Apply filters based on form data
        if state:
            available_workers = available_workers.filter(state=state)
        
        if district:
            available_workers = available_workers.filter(district=district)
        
        if work_type:
            available_workers = available_workers.filter(services__icontains=work_type)

        # If booking date is provided, exclude workers who are already booked
        if booking_date:
            try:
                booking_date = datetime.strptime(booking_date, '%Y-%m-%d').date()
                booked_workers = Bookings.objects.filter(
                    booking_date=booking_date
                ).values_list('worker_id', flat=True)
                
                available_workers = available_workers.exclude(
                    id__in=booked_workers
                )
            except ValueError:
                pass  # Handle invalid date format

        # Render only the worker list partial template
        html = render_to_string(
            'bookings.html',
            {
                'available_workers': available_workers,
                'selected_date': booking_date,
            },
            request=request
        )
        return HttpResponse(html)

    # Regular form GET request
    worker_types = Service_Details.objects.values_list('service_name', flat=True).distinct()
    context = {
        'worker_types': worker_types,
    }
    return render(request, 'bookings.html', context)



def my_bookings(request):
    # Fetch bookings related to the logged-in user
    bookings = Bookings.objects.filter(user=request.session.get('user_id'))

    context = {
        'bookings': bookings
    }
    return render(request, 'my_bookings.html', context)


from .models import Bookings  # Make sure 'Booking' is the correct model name
from datetime import datetime
from .models import Bookings  # Import the model

def manage_bookings(request):
    if request.session.get('is_admin'):  # Check if user is admin
        bookings = Bookings.objects.select_related('user').all()  # Fetch all bookings from the database
        context = {
            'bookings': bookings,
            'current_year': datetime.now().year,  # Add current year for footer
        }
        return render(request, 'manage_bookings.html', context)
    else:
        return redirect('admin_login')  # Redirect to login if not admin
    
from .models import Service_Details
def manage_services(request):
    if request.session.get ('is_admin'):
        services = Service_Details.objects.all()  # Fetch all services
    return render(request, 'manage_services.html', {'services': services})



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

from django.shortcuts import render, redirect
from .models import Service_Details
from django.contrib import messages

def add_service(request):
    if request.method == "POST":
        service_image = request.FILES.get('service_image')
        service_name = request.POST.get('service_name')
        description = request.POST.get('description')
        price = request.POST.get('price')

        service = Service_Details(
            service_image=service_image,
            service_name=service_name,
            description=description,
            price=price
        )
        service.save()
        messages.success(request, 'Service added successfully!')
        return redirect('add_service')  # Redirect to the same page or another page after adding the service

    return render(request, 'add_service.html')

def delete_service(request, service_id):
    if request.method == "POST":
        service = get_object_or_404(Service_Details, id=service_id)
        service.delete()
        messages.success(request, "Service deleted successfully.")
        return redirect('manage_services')  # Replace 'manage_services' with the actual name of your view/page
    else:
        messages.error(request, "Invalid request method.")
        return redirect('manage_services')

def edit_service(request, service_id):
    service = get_object_or_404(Service_Details, id=service_id)

    if request.method == 'POST':
        service_name = request.POST.get('service_name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        service_image = request.FILES.get('service_image')

        # Validate and update the service
        if service_image and not service_image.name.endswith(('.png', '.jpg', '.jpeg')):
            messages.error(request, "Service image must be a PNG or JPG file.")
            return redirect('edit_service', service_id=service.id)

        service.service_name = service_name
        service.description = description
        service.price = float(price)  # Convert price to float

        if service_image:
            service.service_image = service_image

        service.save()
        messages.success(request, "Service updated successfully!")
        return redirect('manage_services')

    return render(request, 'edit_service.html', {'service': service})
# HomeServices/myapp/views.py
from django.shortcuts import render, redirect
from .models import Service_Details, ServiceList

##############SUBSERVICELIST###############

def add_service_list(request):
    if not request.session.get('is_admin'):
        return redirect('login')
    if request.method == 'POST':
        service_detail = Service_Details.objects.get(id=request.POST['service_detail'])
        sub_service_name = request.POST['sub_service_name']
        description = request.POST['description']
        rate = request.POST['rate']
        image = request.FILES.get('image')
        

        ServiceList.objects.create(
            service_detail=service_detail,
            sub_service_name=sub_service_name,
            description=description,
            rate=rate,
            image=image
        )
         # Redirect to the same page or another page

    service_details = Service_Details.objects.all()
    return render(request, 'add_service_list.html', {'service_details': service_details})

def service_details(request, service_id):# Fetch the service details using get_object_or_404 for better error handling
    service = get_object_or_404(Service_Details, id=service_id)# Fetch the related sub-services from ServiceList
    sub_services = ServiceList.objects.filter(service_detail=service)# Render the service details template with both service and sub-services
    return render(request, 'service_details.html', {'service': service, 'sub_services': sub_services})


def servicelist(request):
    services = Service_Details.objects.all()
    return render(request, 'service_list.html', {'services': services})
from .models import ServiceList  # Ensure you import your ServiceList model

def manage_subservice(request):
       sub_services = ServiceList.objects.all()  # Fetch all sub-services
       print(sub_services)
       return render(request, 'manage_subservice.html', {'sub_services': sub_services})

def edit_subservice(request, sub_service_id):
    sub_service = get_object_or_404(ServiceList, id=sub_service_id)

    if request.method == 'POST':
        sub_service_name = request.POST.get('sub_service_name')
        description = request.POST.get('description')
        rate = request.POST.get('rate')
        image = request.FILES.get('image')  # Get the uploaded image

        sub_service.sub_service_name = sub_service_name
        sub_service.description = description
        sub_service.rate = rate
        
        # Only update image if a new one was uploaded
        if image:
            sub_service.image = image
            
        sub_service.save()

        messages.success(request, "Sub-Service updated successfully!")
        return redirect('manage_subservice')

    return render(request, 'edit_subservice.html', {'sub_service': sub_service})

def delete_subservice(request, sub_service_id):
    sub_service = get_object_or_404(ServiceList, id=sub_service_id)
    sub_service.delete()
    messages.success(request, "Sub-Service deleted successfully!")
    return redirect('manage_subservice')



from django.shortcuts import render, redirect
from .models import Announcement
from django.contrib import messages
from django.utils import timezone

def add_announcement(request):
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        expires_at = request.POST.get('expires_at')

        Announcement.objects.create(
            title=title,
            content=content,
            expires_at=expires_at
        )
        messages.success(request, 'Announcement added successfully!')
        return redirect('admin_dashboard')

    return render(request, 'add_announcement.html')

from .models import Announcement
from django.contrib import messages

def view_announcements(request):
    announcements = Announcement.objects.all().order_by('-created_at')
    return render(request, 'view_announcements.html', {'announcements': announcements})

def delete_announcement(request, announcement_id):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    announcement.delete()
    messages.success(request, 'Announcement deleted successfully.')
    return redirect('view_announcements')

import os
from django.conf import settings
from django.http import FileResponse, Http404

def certificate_view(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'HomeServices', 'certificates', filename)
    print(f"Attempting to access file: {file_path}")
    print(f"File exists: {os.path.exists(file_path)}")
    print(f"Directory contents: {os.listdir(os.path.dirname(file_path))}")
    try:
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        print(f"File not found: {file_path}")

import os
from django.http import FileResponse, Http404
from django.conf import settings

def resume_view(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'HomeServices', 'resumes', filename)

    # Check if the file exists
    if os.path.exists(file_path):
        try:
            response = FileResponse(open(file_path, 'rb'), content_type='resumes/pdf')
            response['Content-Disposition'] = 'inline; filename="{}"'.format(filename)  # Set to 'inline' to view in browser
            return response
        except Exception as e:
            raise Http404("Error occurred while opening the file")
    else:
        raise Http404("Resume not found")


def profile_image_view(request, filename):
    file_path = os.path.join(settings.BASE_DIR, 'HomeServices', 'profile_images', filename)
    try:
        return FileResponse(open(file_path, 'rb'), content_type='image/jpeg')  # Adjust content type if needed
    except FileNotFoundError:
        raise Http404()
        

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from openai import OpenAI  # Import the OpenAI client

# Set your OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')
# Your DeepAI API key

# Configure logging
logger = logging.getLogger(__name__)

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

@csrf_exempt  # Disable CSRF for this view (use with caution)
def chatbot_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')

        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        try:
            # Call the AI service to get a response
            completion = client.chat.completions.create(
                model="gpt-4o-mini",  # Use the appropriate model
                messages=[{"role": "user", "content": user_message}]
            )

            # Log the full response for debugging
            logger.info(f"OpenAI response: {completion}")

            # Check if choices are available
            if not completion.choices:
                return JsonResponse({'error': 'No response from AI'}, status=500)

            # Extract the AI's response using dot notation
            ai_message = completion.choices[0].message.content  # Use dot notation here
            return JsonResponse({'response': ai_message})

        except Exception as e:
            logger.error(f"Error fetching response from OpenAI: {e}")
            return JsonResponse({'error': 'Failed to get response from AI'}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)




# HomeServices/myapp/views.py

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Bookings
from django.views.decorators.http import require_POST

@require_POST
def accept_booking(request, booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
        booking.status = 'accepted'
        booking.save()
        return JsonResponse({'status': 'success'})
    except Bookings.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)

from django.utils import timezone
from datetime import datetime
from django.views.decorators.http import require_POST

@require_POST
def request_start_timer(request, booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
        booking.status = 'timer_requested'
        booking.save()
        return JsonResponse({'status': 'success'})
    except Bookings.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)

@require_POST
def request_stop_timer(request, booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
        booking.status = 'stop_requested'
        booking.timer_end = timezone.now()
        
        # Calculate and save the working time if timer_start exists
        if booking.timer_start:
            # Calculate duration between start and end time
            duration = booking.timer_end - booking.timer_start
            booking.working_time = duration
            
            # Log the times for verification
            print(f"Timer Start: {booking.timer_start}")
            print(f"Timer End: {booking.timer_end}")
            print(f"Working Time: {duration}")
        
        booking.save()
        return JsonResponse({
            'status': 'success',
            'working_time': str(booking.working_time) if booking.working_time else None
        })
    except Bookings.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

def get_timer_start(request, booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
        if booking.timer_start:
            return JsonResponse({'timer_start': booking.timer_start.isoformat()})
        return JsonResponse({'timer_start': None})
    except Bookings.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)

@require_POST
def start_timer(request, booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
        booking.status = 'in_progress'
        booking.timer_start = timezone.now()
        booking.save()
        return JsonResponse({'status': 'success'})
    except Bookings.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)

@require_POST
def accept_timer_start(request, booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
        booking.status = 'in_progress'
        booking.timer_start = timezone.now()
        booking.save()
        return JsonResponse({'status': 'success'})
    except Bookings.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)

@require_POST
def reject_timer_start(request, booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
        booking.status = 'accepted'  # Revert to accepted status
        booking.save()
        return JsonResponse({'status': 'success'})
    except Bookings.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)

@require_POST
def confirm_stop_timer(request, booking_id):
    try:
        print(f"Confirming stop timer for booking {booking_id}")  # Debug log
        booking = Bookings.objects.get(id=booking_id)
        
        print(f"Current status: {booking.status}")  # Debug log
        booking.status = 'completed'
        
        # Ensure timer_end is set
        if not booking.timer_end:
            booking.timer_end = timezone.now()
        
        # Calculate final working time if not already set
        if booking.timer_start and not booking.working_time:
            booking.working_time = booking.timer_end - booking.timer_start
            print(f"Calculated working time: {booking.working_time}")  # Debug log
        
        # Update worker status to available
        if booking.worker:
            booking.worker.status = "Available"
            booking.worker.save()
            print(f"Updated worker status to Available")  # Debug log
        
        booking.save()
        print(f"Booking saved successfully")  # Debug log
        
        return JsonResponse({
            'status': 'success',
            'working_time': str(booking.working_time) if booking.working_time else None
        })
    except Bookings.DoesNotExist:
        print(f"Booking {booking_id} not found")  # Debug log
        return JsonResponse({
            'status': 'error', 
            'message': 'Booking not found'
        }, status=404)
    except Exception as e:
        print(f"Error in confirm_stop_timer: {str(e)}")  # Debug log
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_POST
def reject_stop_timer(request, booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
        booking.status = 'in_progress'  # Revert to in_progress
        booking.timer_end = None  # Clear the end time
        booking.working_time = None  # Clear the working time
        booking.save()
        return JsonResponse({'status': 'success'})
    except Bookings.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Booking not found'}, status=404)

def send_bill(request, booking_id):
    try:
        booking = Bookings.objects.get(id=booking_id)
        service = Service_Details.objects.get(service_name=booking.work)
        
        # Calculate total hours worked
        total_hours = booking.working_time.total_seconds() / 3600  # Convert to hours
        rate_per_hour = float(service.price)
        total_amount = rate_per_hour * total_hours
        
        context = {
            'booking': booking,
            'service': service,
            'total_hours': round(total_hours, 2),
            'rate_per_hour': rate_per_hour,
            'total_amount': round(total_amount, 2),
            'working_time': booking.working_time
        }
        
        if request.method == 'POST':
            # Create payment record with uploaded files
            payment = Payment.objects.create(
                booking=booking,
                amount=round(total_amount, 2),
                rate_per_hour=rate_per_hour,
                total_hours=round(total_hours, 2),
                payment_status='pending',
                additional_notes=request.POST.get('additional_notes', ''),
                work_completion_image=request.FILES.get('work_completion_image'),
                work_completion_video=request.FILES.get('work_completion_video')
            )
            
            # Create bill content
            bill_content = f"""
            Bill for Service

            Service: {booking.work}
            Worker: {booking.worker.worker_name}
            Date: {booking.booking_date}
            Working Time: {booking.working_time}
            Rate per Hour: ₹{rate_per_hour}
            Total Hours: {round(total_hours, 2)}
            Total Amount: ₹{round(total_amount, 2)}

            Address: {booking.address_line}, {booking.city}
            Phone: {booking.phone_number}
            
            Payment ID: {payment.id}
            
            Additional Notes:
            {request.POST.get('additional_notes', '')}
            
            Thank you for using our service!
            """
            
            # Send email
            send_mail(
                subject=f'Bill for {booking.work} Service',
                message=bill_content,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[booking.user.email],
                fail_silently=False,
            )
            
            # Update booking status
            booking.status = 'billed'
            booking.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Bill sent successfully'
            })
        
        # Handle GET request (showing the form)
        return render(request, 'send_bill.html', context)
        
    except Exception as e:
        print(f"Error in send_bill: {str(e)}")  # Debug log
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

def payment_history(request):
    # Check if user is logged in via session
    worker_id = request.session.get('worker_id')
    if not worker_id:
        return redirect('login')
    
    # Get all payments for bookings assigned to this worker
    payments = Payment.objects.filter(
        booking__worker_id=worker_id
    ).order_by('-payment_date')
    
    context = {
        'payments': payments,
        'username': request.session.get('user_name', 'Guest')
    }
    
    return render(request, 'payment_history.html', context)

def user_payment_history(request):
    # Get the user's ID from the session
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('login')
    
    # Get all payments for bookings made by this user
    payments = Payment.objects.filter(
        booking__user_id=user_id
    ).order_by('-payment_date')
    
    return render(request, 'user_payment_history.html', {
        'payments': payments,
        'username': request.session.get('user_name', 'Guest')
    })

import razorpay
from django.conf import settings

def initiate_payment(request, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)
        
        # Initialize Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET_KEY))
        
        # Create Razorpay order
        payment_amount = int(float(payment.amount) * 100)  # Convert to paise
        razorpay_order = client.order.create({
            'amount': payment_amount,
            'currency': 'INR',
            'payment_capture': 1
        })
        
        # Update payment with razorpay order id
        payment.razorpay_order_id = razorpay_order['id']
        payment.save()
        
        context = {
            'payment': payment,
            'razorpay_key': settings.RAZORPAY_API_KEY,
            'razorpay_order_id': razorpay_order['id'],
            'callback_url': request.build_absolute_uri(reverse('payment_callback')),
            'amount': payment_amount,
            'currency': 'INR',
            'email': payment.booking.user.email,
            'username': payment.booking.user.username,
        }
        
        return render(request, 'pay_now.html', context)
        
    except Payment.DoesNotExist:
        return JsonResponse({'error': 'Payment not found'}, status=404)

@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        try:
            # Get payment data
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            
            # Initialize Razorpay client
            client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_SECRET_KEY))
            
            # Verify payment signature
            params_dict = {
                'razorpay_payment_id': payment_id,
                'razorpay_order_id': razorpay_order_id,
                'razorpay_signature': signature
            }
            
            try:
                client.utility.verify_payment_signature(params_dict)
                # Update payment status
                payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
                payment.payment_status = 'completed'
                payment.razorpay_payment_id = payment_id
                payment.save()
                
                return JsonResponse({'status': 'success'})
            except:
                return JsonResponse({'status': 'failed'})
                
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'invalid request'})
#################################################################################################
#######_SMART_DETECTION_######################3
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
from reportlab.lib import colors
from django.core.files.base import ContentFile
import io
from django.utils import timezone
import base64
import google.generativeai as genai

try:
    import google.generativeai as genai
    # Configure Gemini AI
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

    
    # Test available models
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)
            
except ImportError:
    print("Please install google-generativeai package using: pip install google-generativeai")
    raise



@csrf_exempt
def detect_service(request):
    if request.method == 'POST':
        try:
            print("Received request")  # Debug print
            image = request.FILES.get('image')
            if not image:
                print("No image in request")  # Debug print
                return JsonResponse({'error': 'No image provided'}, status=400)

            print(f"Image received: {image.name}")  # Debug print

            # Configure the API key
            genai.configure(api_key=settings.GEMINI_API_KEY)

            # Read image bytes
            image_bytes = image.read()
            
            # Initialize Gemini Vision model with the latest version
            model = genai.GenerativeModel('gemini-1.5-flash')  # Updated to the latest model
            
            # Create content parts
            contents = [
                {
                    "parts": [
                        {
                            "text": """
                            Analyze this image and provide a brief, concise response in the following format:

                            🔍 Problem:
                            [Short description of the visible damage/issue in 1-2 sentences]

                            👨‍🔧 Service Provider:
                            • Type: [Carpenter/Plumber/Electrician/Appliance Technician]
                            • Expertise: [Basic/Expert]
                            • Cost: [$XX - $XX]
                            • DIY: [Yes/No]

                            📝 Quick Fix Steps (3-4 steps max):
                            1. [Brief step]
                            2. [Brief step]
                            3. [Brief step]

                            ⚠️ Safety:
                            • [2-3 key safety points only]
                            • [Required tools]

                            Keep all responses brief and actionable. Use simple language.
                            """
                        },
                        {
                            "inline_data": {
                                "mime_type": image.content_type,
                                "data": base64.b64encode(image_bytes).decode('utf-8')
                            }
                        }
                    ]
                }
            ]
            
            print("Sending request to Gemini")  # Debug print
            
            # Generate response
            response = model.generate_content(contents)
            
            if not response:
                print("No response from model")  # Debug print
                raise Exception("No response from AI model")

            print("Got response from model")  # Debug print
            
            return JsonResponse({
                'problem': response.text
            })
            
        except Exception as e:
            print(f"Error in service detection: {str(e)}")  # Debug print
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def smart_view(request):
    # Get the username for the home template
    username = request.user.username if request.user.is_authenticated else None
    return render(request, 'smart_detection.html', {'username': username})
#pip install google-generativeai
#pip install PyPDF2 python-docx python-pptx
#pip install reportlab
# views.py
from django.http import JsonResponse
from django.utils import timezone

def get_booking_status(request):
    try:
        # Get the latest booking for the current user
        latest_booking = Booking.objects.filter(
            user=request.user
        ).select_related(
            'service',
            'worker'
        ).latest('created_at')

        return JsonResponse({
            'currentStep': latest_booking.status,
            'service_type': latest_booking.service.service_name,
            'worker_name': f"{latest_booking.worker.first_name} {latest_booking.worker.last_name}",
            'location': latest_booking.service_location,
            'price': str(latest_booking.service.price),
            'booking_date': latest_booking.created_at.strftime('%B %d, %Y at %I:%M %p'),
            'status_message': latest_booking.status_message,  # If you have any custom status message
        })
    except Booking.DoesNotExist:
        return JsonResponse({
            'error': 'No booking found',
            'currentStep': 'none'
        }, status=404)

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import WorkerLocation, Bookings
import json

@csrf_exempt
@require_http_methods(["POST"])
def start_location_sharing(request):
    try:
        data = json.loads(request.body)
        worker_id = data.get('worker_id')
        booking_id = data.get('booking_id')
        latitude = data.get('latitude', 0)
        longitude = data.get('longitude', 0)

        # Create or update worker location with sharing enabled
        location, created = WorkerLocation.objects.update_or_create(
            worker_id=worker_id,
            booking_id=booking_id,
            defaults={
                'latitude': latitude,
                'longitude': longitude,
                'is_sharing': True
            }
        )

        # Default destination (Kottayam coordinates)
        destination = {
            'lat': 9.5916,
            'lng': 76.5222
        }

        return JsonResponse({
            'success': True,
            'message': 'Location sharing started',
            'destination': destination
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

@require_http_methods(["GET"])
def get_worker_location(request, worker_id, booking_id):
    try:
        location = WorkerLocation.objects.filter(
            worker_id=worker_id,
            booking_id=booking_id,
            is_sharing=True
        ).latest('timestamp')

        # Default destination (Kottayam)
        destination = {
            'lat': 9.5916,
            'lng': 76.5222,
            'name': 'Kottayam'
        }

        return JsonResponse({
            'success': True,
            'latitude': float(location.latitude),
            'longitude': float(location.longitude),
            'destination': destination,
            'last_updated': location.timestamp.strftime('%H:%M:%S')
        })
    except WorkerLocation.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Location not found'
        }, status=404)

