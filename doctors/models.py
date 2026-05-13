from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    specialization = models.CharField(max_length=100)
    fee = models.DecimalField(max_digits=10, decimal_places=2)

    # ✅ New fields
    experience = models.PositiveIntegerField(default=0)
    languages = models.CharField(max_length=200, blank=True)
    image = models.ImageField(upload_to='doctors/', blank=True, null=True)

    about = models.TextField(blank=True)

    def __str__(self):
        return f"Dr. {self.user}"