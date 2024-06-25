from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .constants import PLATFORMS, DEVICES


class Nationality(models.Model):
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UserAttr(models.Model):
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    xbox_id = models.CharField(max_length=50, blank=True, null=True, unique=True)
    nationality = models.ForeignKey(Nationality, on_delete=models.SET_NULL, null=True, blank=True)
    platform = models.CharField(max_length=10, choices=PLATFORMS, blank=True, null=True)
    device = models.CharField(max_length=10, choices=DEVICES, blank=True, null=True)
    forza_rating = models.IntegerField(default=1000, validators=[
        MinValueValidator(0), MaxValueValidator(5000)
    ])
    forza_safety_rating = models.IntegerField(default=1000, validators=[
        MinValueValidator(0), MaxValueValidator(5000)
    ])
    youtube_url = models.URLField(max_length=200, blank=True, null=True)
    twitch_url = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.xbox_id


class CustomUser(AbstractUser):
    user_attr = models.OneToOneField(UserAttr, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='custom_user')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='customuser',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username


@receiver(post_save, sender=CustomUser)
def create_user_attr(sender, instance, created, **kwargs):
    if created:
        UserAttr.objects.create(user=instance)


@receiver(post_save, sender=CustomUser)
def save_user_attr(sender, instance, **kwargs):
    instance.userattr.save()
