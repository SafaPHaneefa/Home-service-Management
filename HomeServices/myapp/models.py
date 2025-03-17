from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.utils import timezone
  
    
    
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

class ServiceList(models.Model):
    service_detail = models.ForeignKey(Service_Details, on_delete=models.CASCADE, related_name='service_lists')
    sub_service_name = models.CharField(max_length=150)
    description = models.TextField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='sub_service_images/', null=True, blank=True)

    def __str__(self):
        return self.sub_service_name
    
# HomeServices/myapp/models.py

from django.db import models

class Bookings(models.Model):
    # ForeignKey to associate the booking with a user (worker)
    user = models.ForeignKey(users, on_delete=models.CASCADE, related_name='bookings')
    worker = models.ForeignKey(Workers_Details, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    
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
    work = models.CharField(max_length=100)

    # Update status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('timer_requested', 'Timer Requested'),
        ('in_progress', 'In Progress'),
        ('stop_requested', 'Stop Requested'),
        ('completed', 'Completed'),
        ('billed', 'Billed')
    ]
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending'
    )
    
    timer_start = models.DateTimeField(null=True, blank=True)
    timer_end = models.DateTimeField(null=True, blank=True)

    # New field for tracking working time
    working_time = models.DurationField(null=True, blank=True)  # To store the total working time

    # Additional fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
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
    

class Payment(models.Model):
    booking = models.ForeignKey(Bookings, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    rate_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    total_hours = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=20, default='pending')  # pending, completed, failed
    additional_notes = models.TextField(blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    
    # New fields for work completion media
    work_completion_image = models.ImageField(upload_to='work_completion_images/', null=True, blank=True)
    work_completion_video = models.FileField(upload_to='work_completion_videos/', null=True, blank=True)

    def __str__(self):
        return f"Payment for Booking {self.booking.id} - ₹{self.amount}"
    



class WorkerLocation(models.Model):
    worker = models.ForeignKey('Workers_Details', on_delete=models.CASCADE)
    booking = models.ForeignKey('Bookings', on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_sharing = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        get_latest_by = 'timestamp'

    def __str__(self):
        return f"Location of {self.worker.worker_name} for booking {self.booking.id}"