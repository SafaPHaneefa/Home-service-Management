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
      # Output the username for debugging
    return render(request, 'home.html', {'username': username,'active_announcements': active_announcements})
    

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

    if request.method == 'POST':
        # Get form data
        worker_name = request.POST.get('worker_name')
        profile_image = request.FILES.get('profile_image')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        pincode = request.POST.get('pincode')
        phone_no = request.POST.get('phone_no')
        experience = request.POST.get('experience')
        certificate = request.FILES.get('certificate')
        services_selected = request.POST.getlist('services')
        resume = request.FILES.get('resume')

        # Email validation (check if it exists or is invalid)
        if Workers_Details.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('worker_registration')
        try:
            validate_email(email)  # Check if the email is in the correct format
        except ValidationError:
            messages.error(request, "Invalid email format!")
            return redirect('worker_registration')

        if len(phone_no) != 10 or not phone_no.isdigit():
            messages.error(request, "Phone number must be 10 digits!")
            return redirect('worker_registration')
        dob_datetime = datetime.strptime(dob, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - dob_datetime.year - ((today.month, today.day) < (dob_datetime.month, dob_datetime.day))
        if age < 18:
            messages.error(request, "You must be at least 18 years old to register!")
            return redirect('worker_registration')

        worker = Workers_Details(
            worker_name=worker_name,
            profile_image=profile_image,
            email=email,
            gender=gender,
            dob=dob,
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
    
    
    