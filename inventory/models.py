from django.db import models

class BloodInventory(models.Model):
    blood_group = models.CharField(max_length=5)
    units_available = models.IntegerField()

    def __str__(self):
        return f"{self.blood_group} - {self.units_available}"