from django.db import models
from accounts.models import CustomUser


# 🔹 Recipient Model
class Recipient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hospital_name = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


# 🔹 Blood Request Model
class BloodRequest(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blood_group = models.CharField(max_length=5)
    units = models.IntegerField()
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.blood_group}"