from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    # Add custom fields here if needed
    phone_number = models.CharField(_('Phone Number'), max_length=15, blank=True)
    profile_picture = models.ImageField(_('Profile Picture'), upload_to='profiles/', blank=True)
    date_of_birth = models.DateField(_('Date of Birth'), null=True, blank=True)
    
    # Add any additional fields you need
    
    def __str__(self):
        return self.email or self.username