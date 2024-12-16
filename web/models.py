from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.utils.text import slugify

import uuid
from datetime import timedelta
from dateutil.relativedelta import relativedelta


# user table--------------------------------------------------------------------
class MyUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("email is required")
        if not username:
            raise ValueError("Your user name is required")
        if not first_name:
            raise ValueError("Your First Name is required")
        if not last_name:
            raise ValueError("Your Last Name is required")
        
        

        user=self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            
            
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, username, first_name, last_name, password=None):
        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,

        )
        user.is_admin=True
        user.is_staff=True
        
        user.is_superuser=True
        user.save(using=self._db)
        return user

     

class MyUser(AbstractBaseUser):
    email=models.EmailField(verbose_name="email", max_length=100, unique=True)
    first_name=models.CharField(verbose_name="first name", max_length=100, unique=False)
    username=models.CharField(verbose_name="user name", max_length=100, unique=True)
    
    last_name=models.CharField(verbose_name="last name", max_length=100, unique=False)
    
    date_joined=models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    
    last_login=models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=True)
    hide_email = models.BooleanField(default=True)
    


    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['username']
    
    objects=MyUserManager()

    def __str__(self):
        return self.username

    


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

# end user table -------------
# Create your models here.
class Contact(models.Model):
    Full_Name = models.CharField(max_length=100, null=True)
    Email = models.EmailField(max_length=200, null=True)
    Phone = models.CharField(max_length=100, null=True)
    Message = models.CharField(max_length=100, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

 # ROOM MODELS
class Room(models.Model):
    room_number = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
    )
    Room_Name = models.CharField(max_length=100)
    Room_Number = models.CharField(max_length=10, choices=room_number)
    Image =models.ImageField(upload_to="home/")
    Cost = models.DecimalField(max_digits=10, decimal_places=2)
    Post_date = models.DateTimeField(auto_now_add=True)


# MY_PRODUCT MODELS
class MyPayment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('expired', 'expired'),
    )
    
    MONTH_CHOICES = (
        (3, '3 Months'),
        (6, '6 Months'),
    )
    
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Room_Name = models.CharField(max_length=100)
    Cost = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100)
    Payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    Month = models.IntegerField(choices=MONTH_CHOICES)  # Changed to IntegerField
    Payment_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)  # Allow end_date to be null initially
    
    unique_code = models.CharField(max_length=100, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate unique code if not present
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4()).replace('-', '')[:12]  # Generate a unique 12-character code
        
        # Calculate end_date based on Payment_date and Month
        if not self.end_date:
            # Add the exact number of months to the Payment_date
            self.end_date = self.Payment_date + relativedelta(months=self.Month)

        # Save the object
        super().save(*args, **kwargs)

        
        
# PAYMENT MODELS
class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('paid', 'Paid'),
        ('pending', 'Pending'),
        ('failed', 'Failed'),
    )
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Cost = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    Payment_date = models.DateTimeField(auto_now_add=True)
    End_date = models.DateTimeField(auto_now_add=True)

    