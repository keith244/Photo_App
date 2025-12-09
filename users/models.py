from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.contrib.auth.hashers import make_password
from django.conf import settings
# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self,username,email,password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be provided')
        if not email:
            raise ValueError('The email field must be provided')
        
        
        email = self.normalize_email(email)
        user = self.model(username = username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_superuser(self,username,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(username,email, password, **extra_fields)
    
class User(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default= True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        if self.pk:
            self.save(update_fields=['password'])
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    about = models.TextField(max_length=500, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'
    class Meta:
        verbose_name_plural = 'User Profiles'
