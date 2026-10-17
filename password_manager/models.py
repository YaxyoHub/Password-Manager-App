import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta

AMAL_QILISH_MUDDATI = timedelta(minutes=10)

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Foydalanuvchi email kiritilishi shart')
        if not username:
            raise ValueError('Foydalanuvchi nomi kiritilishi shart')
        
        n_email = self.normalize_email(email)
        user = self.model(username=username, email=n_email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username=username, email=email, password=password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(unique=True, max_length=16)
    email = models.EmailField(unique=True, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)   
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    
    def str(self):
        return self.username

class OTP_codes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    code = models.CharField(max_length=32)
    is_used = models.BooleanField(default=False)
    expiration_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.expiration_time:
            self.expiration_time = timezone.now() + AMAL_QILISH_MUDDATI
            
    @property
    def muddat_tekshirish(self):
        return timezone.now() >= self.expiration_time

    def str(self):
        return f"{self.user_id.username} - {self.code}"
    
class App_Password(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    website_name = models.CharField(max_length=255)
    link = models.URLField(max_length=255)
    app_password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user_id.username} - {self.website_name}"