from django.db import models
from django.contrib.auth.models import AbstractUser
from uuid import uuid4
# Create your models here.

class User(AbstractUser):    
    first_name = models.CharField(max_length= 255)
    last_name =  models.CharField(max_length= 255)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length= 255, unique=True)
    password = models.CharField(max_length = 255)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
