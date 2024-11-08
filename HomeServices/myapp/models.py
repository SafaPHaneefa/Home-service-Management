from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
  
    
    
class users(models.Model):
    username=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    password=models.CharField(max_length=150)
    role=models.CharField(max_length=150)
    worker_id=models.CharField(max_length=150,default='none')
    status=models.CharField(max_length=150,default='approved')
    is_active=models.BooleanField(default=False)



class Feedback(models.Model):
    # ForeignKey to associate the feedback with a registered user
    user = models.ForeignKey(users, on_delete=models.CASCADE, related_name='feedbacks')

    # Fields for rating (1 to 5 stars) and description
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Provide a rating between 1 (worst) and 5 (best)."
    )
    description = models.TextField(max_length=500, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.rating} Stars by {self.user.username}"
    

class Workers_Details(models.Model):
    worker_name = models.CharField(max_length=150)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)  
    email = models.EmailField(max_length=150)
    gender = models.CharField(max_length=10)  
    dob = models.DateField() 
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.TextField() 
    pincode=models.CharField(max_length=150) 
    phone_no = models.CharField(max_length=15)
    experience = models.CharField(max_length=150) 
    certificate = models.FileField(upload_to='certificates/', null=True, blank=True) 
    services = models.TextField() 
    resume = models.FileField(upload_to='resumes/', null=True, blank=True) 
    is_active = models.BooleanField(default=False)
    status = models.CharField(max_length=100,default="Available") 

    def __str__(self):
        return self.worker_name
class Service_Details(models.Model):
    service_image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    service_name = models.CharField(max_length=150)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

def __str__(self):
        return self.service_name
    

class Bookings(models.Model):
    # ForeignKey to associate the booking with a user (worker)
    user = models.ForeignKey(users, on_delete=models.CASCADE, related_name='bookings')  # Add this line
    worker=models.ForeignKey(Workers_Details, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True) 
    # Fields for Booking Date, ensuring Sundays are not selectable
    booking_date = models.DateField()

    # Address fields
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street_number = models.CharField(max_length=100)
    address_line = models.CharField(max_length=200, blank=True, null=True)

    # Time field
    booking_time = models.TimeField()

    # Field for Work Type
    work = models.CharField(max_length=100)  # Store the type of work (e.g., electrician, plumber, etc.)

    # Additional fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    work_description = models.TextField()

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.work} Booking on {self.booking_date} at {self.booking_time} by {self.user.username}"
    
from django.utils import timezone

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_active(self):
        return timezone.now() < self.expires_at