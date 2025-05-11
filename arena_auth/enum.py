from django.db import models


class Platform(models.TextChoices):
    PC = 'PC'
    Xbox = 'Xbox'


class Devices(models.TextChoices):
    WHEEL = 'Wheel'
    CONTROLLER = 'Controller'


class UserRole(models.TextChoices):
    MANAGER = 'MANAGER'
    SUPERVISOR = 'SUPERVISOR'
    CREATOR = 'CREATOR'
    MEMBER = 'MEMBER'
    ADMIN = 'ADMIN'
