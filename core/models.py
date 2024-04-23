from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
import uuid

class managment(models.Model):  
    name = models.CharField(max_length=100)


class Patient(models.Model):
    GENDER_TABLE =(
        ('M', 'Male'),
        ('F', 'Female'),
    )
    BLOOD_TABLE=(
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    photo = models.ImageField(upload_to='patient_images/',null=True, blank=True)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDER_TABLE)
    blood = models.CharField(max_length=3, choices=BLOOD_TABLE)
    patient_status = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"


class Pharmacy(models.Model):  
    contact_number = models.CharField(max_length=15)
    location= models.CharField(max_length=20)
    name= models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} {self.location}"
    
    
class Pharmacist(models.Model):  
    contact_number = models.CharField(max_length=15)
    name= models.CharField(max_length=20)
    pharmacyID = models.ForeignKey(Pharmacy, on_delete=models.CASCADE,default=1)
    def __str__(self):
        return f"{self.name} {self.location}"

class Specialty(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self) -> str:
        return self.title
    
class Doctor(models.Model):  
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    address = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='doctor_photos/', null=True, blank=True)
    doctor_price= models.CharField(max_length=15)
    university= models.CharField(max_length=30)
    specialty= models.ForeignKey(Specialty, on_delete=models.CASCADE)
    pharmacyID = models.ForeignKey(Pharmacy, on_delete=models.CASCADE,default=1)


class Refound(models.Model):
    refound_amount=models.DecimalField(max_digits=10, decimal_places=10)


class Reception(models.Model):  
    name= models.CharField(max_length=20)
    refound_id=models.ForeignKey(Refound,on_delete=models.CASCADE)



class Reservation(models.Model):
    data = models.CharField(max_length=15)
    time_slot = models.TimeField()  # Added to store the time of the reservation
    payment_method = models.CharField(max_length=20)
    payment_amount = models.CharField(max_length=20)
    patientID = models.ForeignKey(Patient, on_delete=models.CASCADE, default=1)
    doctorID = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)
    refound_id = models.ForeignKey(Refound, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.data} {self.time_slot} {self.payment_method}"


    def __str__(self):
        return f"{self.data} {self.payment_method}"
    



