from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
  
    
    
class users(models.Model):
    username=models.CharField(max_length=150)
    email=models.CharField(max_length=150)
    password=models.CharField(max_length=150)
    role=models.CharField(max_length=150)
    work=models.CharField(max_length=150)
    status=models.CharField(max_length=150,default='approved')
       