from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


# Create your models here.
#custom model manager
class CustomUserManager(BaseUserManager):
    #creating a user
    def create_user(self,email, nationality,password=None, **extra_fields):
        if not email:
            raise ValueError('The email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, nationality=nationality, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    #creating a super user
    def create_superuser(self,email, nationality ,password=None, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get ('is_staff') is not True:
            raise ValueError('Superuser must have is staff true ')
        if extra_fields.get ('is_superuser') is not True:
            raise ValueError('Superuser must have is is superuser true ')
        
        return self.create_user(email, nationality,password, **extra_fields)

#custom user model
class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(('Email Address'), unique =True)
    nationality = models.CharField('Nationality',max_length=100)
    is_staff =models.BooleanField(default=False)
    is_active =models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nationality']

    objects = CustomUserManager() # set default model manager for custom user

    def __str__(self): #to be able to view user emails in admin panel 
        return self.email