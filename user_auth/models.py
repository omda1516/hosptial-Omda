from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from django.contrib.auth.models import Permission
from rest_framework_simplejwt.tokens import RefreshToken

class HospitalUser(AbstractUser):
    GENDERS = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    gender = models.CharField(choices=GENDERS, max_length=20)

    # Specify unique related_names for groups and user_permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="hospital_user_set",  # Unique related_name
        related_query_name="hospital_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="hospital_user_set",  # Unique related_name
        related_query_name="hospital_user_permission",
    )

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
