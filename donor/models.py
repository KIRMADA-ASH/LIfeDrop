from django.db import models
from accounts.models import CustomUser

class Donor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    last_donation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username