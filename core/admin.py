
from django.contrib import admin
from core.models import Doctor,  Patient, Pharmacy, Refound, Reception, Specialty,Reservation


admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Pharmacy)
admin.site.register(Refound)
admin.site.register(Reception)
admin.site.register(Specialty)
admin.site.register(Reservation)
