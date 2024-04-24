from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from rest_framework_simplejwt.tokens import RefreshToken

class HospitalUser(AbstractUser):
    GENDERS = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    gender = models.CharField(choices=GENDERS, max_length=20)
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    def in_group(self, group_name):
        """Check if the user is in a specific group."""
        return self.groups.filter(name=group_name).exists()

class DoctorProfile(models.Model):
    user = models.OneToOneField(HospitalUser, on_delete=models.CASCADE, related_name='doctor_profile')
    specialty = models.CharField(max_length=100)
    hospital = models.CharField(max_length=200, blank=True, null=True)  # Optional field for hospital affiliation

    def __str__(self):
        return f"{self.user.username} - {self.specialty}"

class PatientProfile(models.Model):
    user = models.OneToOneField(HospitalUser, on_delete=models.CASCADE, related_name='patient_profile')
    condition = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return f"{self.user.username} - {self.condition}"
