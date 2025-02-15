import json

import uuid
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user manager where email is the unique identifiers
    for authentication instead of usernames.

    Methods:
    - create_user: Create a new user.
    - create_superuser: Create a new superuser.
    """
    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.

        Args:
        - username: The user's username.
        - email: The user's email address.
        - first_name: The user's first name.
        - last_name: The user's last name.
        - password: The user's password.
        - extra_fields: Additional fields to save to the user.

        Returns:
        - user: The newly created user.
        """
        if not email:
            raise ValueError(_('Users must have an email address'))
        if not username:
            raise ValueError(_('Users must have a username'))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.

        Args:
        - username: The user's username.
        - email: The user's email address.
        - first_name: The user's first name.
        - last_name: The user's last name.
        - password: The user's password.
        - extra_fields: Additional fields to save to the user.

        Returns:
        - user: The newly created superuser.
        """
        user = self.create_user(username, email, first_name, last_name, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.admin = True

        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(_('password'), max_length=255, db_column='password_hash')
    admin = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    dark_mode = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    show_friends = models.BooleanField(default=True)
    public_profile = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    opt_out = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False)
    is_to_close = models.BooleanField(default=False)
    api_key = models.CharField(default=str(uuid.uuid4()))
    steam_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    steam_opt_out = models.BooleanField(default=False)
    steam_username = models.CharField(max_length=255, null=True, blank=True)
    use_steam_profile = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f'{self.username} ({self.email})'

    def set_password(self, raw_password):
        """Hashes the password and updates the password field."""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Checks the given raw password against the hashed password."""
        return check_password(raw_password, self.password)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.use_steam_profile:
            self.original_username = self.username
            self.username = self.steam_username

    class Meta:
        db_table = 'users'
        managed = True  # Set to True if Django should manage this table (adjust as needed)
