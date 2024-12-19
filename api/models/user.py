from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_unique_id(self):
        allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        unique_id = get_random_string(length=6, allowed_chars=allowed_chars)
        while self.__class__.objects.filter(id=unique_id).exists():
            unique_id = get_random_string(
                length=6, allowed_chars=allowed_chars)
        return unique_id

    def generate_unique_slug(self, data):
        num = 1
        new_slug = slugify(data)
        while self.__class__.objects.filter(slug=new_slug).exists():
            new_slug = f"{new_slug}-{num}"
            num += 1
        return new_slug

    class Meta:
        abstract = True
        ordering = ['-created_at']


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, password=password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    id = models.CharField(primary_key=True, max_length=6, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250, blank=True)
    fullname = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_suspended = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def set_password(self, raw_password, user=None):
        if not user or user and user.password != self.password:
            super().set_password(raw_password)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()

        user = self.__class__.objects.filter(id=self.id).first()
        # if not user or user and user.password != self.password:
        if not self._password:
            self.set_password(self.password, user)
        self._password = None

        if user and not self.is_staff and self.is_superuser:
            self.is_staff = True

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return f'{self.email} {self.username}'



class Address(BaseModel):
    state = models.CharField(max_length=50)
    address = models.CharField(max_length=500)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_address', null=True)
    