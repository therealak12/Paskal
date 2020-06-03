import uuid
import os

from django.conf import settings
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


def get_avatar_path(instance, file_name):
    """Generate file path for the given file name"""
    return os.path.join('images/user/' + str(instance.id))


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creates and saves a new super user"""
        superuser = self.create_user(email, password, **extra_fields)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email_address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=35, )
    bio = models.CharField(max_length=160, blank=True)
    avatar = models.ImageField(upload_to=get_avatar_path, blank=True, default='images/user/default.png')
    score = models.IntegerField(default=0)
    upvotes = models.ManyToManyField('action.Action', related_name='upvoters')
    downvotes = models.ManyToManyField('action.Action', related_name='downvoters')

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.email



