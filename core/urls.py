from django.urls import path
from . import views

urlpatterns = [
    path("doctors/", views.DoctorList.as_view(), name='doctor-list'),
    path("doctor/<int:pk>", views.DoctorDetail.as_view(), name='doctor-detail'),
    path("Management/", views.ManagementList.as_view(), name='Management-list'),
    path("patients/", views.PatientList.as_view(), name='patient-list'),
    path("patient/<int:pk>", views.PatientDetail.as_view(), name='patient-detail'),
    path('refounds/', views.RefoundListCreateAPIView.as_view(), name='refound-list-create'),
    path('receptions/', views.ReceptionListCreateAPIView.as_view(), name='reception-list-create'),
    path('doctor/<int:doctor_id>/reservations/', views.DoctorReservationAPIView.as_view(), name='doctor-reservations'),
    path('specialties/', views.SpecialtyList.as_view(), name='specialty-list'),
    path('specialties/<int:specialty_id>/doctors/', views.DoctorsBySpecialty.as_view(), name='doctors-by-specialty'),
]

