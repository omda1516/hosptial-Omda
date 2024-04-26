from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Custom user model
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    user_type = models.CharField(max_length=10, choices=[('doctor', 'Doctor'), ('patient', 'Patient'), ('admin', 'Admin')])

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Doctor(CustomUser):
    specialty = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

class Patient(CustomUser):
    blood_type = models.CharField(max_length=3, choices=[('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')])

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'

class Management(CustomUser):
    department = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Management'
        verbose_name_plural = 'Management'

class Pharmacy(models.Model):  
    contact_number = models.CharField(max_length=15)
    location = models.CharField(max_length=20)
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.location}"
    
class Pharmacist(models.Model):  
    contact_number = models.CharField(max_length=15)
    name = models.CharField(max_length=20)
    pharmacyID = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.name} {self.location}"

class Specialty(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.title

class Refound(models.Model):
    refound_amount = models.DecimalField(max_digits=10, decimal_places=10)

class Reception(models.Model):  
    name = models.CharField(max_length=20)
    refound_id = models.ForeignKey(Refound, on_delete=models.CASCADE)

class Reservation(models.Model):
    date = models.CharField(max_length=15)
    time_slot = models.TimeField(default=timezone.now)  # Time of the reservation
    payment_method = models.CharField(max_length=20)
    payment_amount = models.CharField(max_length=20)
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE, default=1)
    doctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)
    refund_id = models.ForeignKey(Refound, on_delete=models.CASCADE)  

    def __str__(self):
        return f"{self.date} {self.time_slot} {self.payment_method}"

    def check_availability(self, date, time_slot):
        count_reservations = Reservation.objects.filter(date=date, doctorID=self.doctorID).count()
        if count_reservations >= 30:
            return False 
        existing_reservation = Reservation.objects.filter(date=date, time_slot=time_slot, doctorID=self.doctorID).exists()
        if existing_reservation:
            return False
        return True



