from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    email = models.EmailField('Email', unique=True)  # Add the email field
    
    # Use the email field for authentication
    USERNAME_FIELD = 'email'
    # Add the email field to the required fields
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.username} ({self.email})'

# class User(AbstractUser):
#     full_name = models.CharField(max_length=100)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  # Add a related_name argument
        related_query_name='custom_user',
        through='UserGroup'  # Specify the intermediate model
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Add a related_name argument
        related_query_name='custom_user',
        through='UserPermission'  # Specify the intermediate model
    )

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)

#Classification history

from django.conf import settings
from django.contrib.auth.models import User

class ClassificationHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    music_file_name = models.CharField(max_length=255)
    classified_genre = models.CharField(max_length=255)
    classification_date = models.DateTimeField(auto_now_add=True)

    # def __str__(self):
    #     return self.file_name