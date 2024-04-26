from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Doctor, Specialty, Management, Patient, Pharmacy, Refound, Reception, Reservation
from .serializers import (
    SpecialtySerializer,
    doctorSerializer,
    ManagmentSerializer,
    PatientSerializer,
    PharmacySerializer,
    ReceptionSerializer,
    RefoundSerializer,
    ReservationSerializer
)
from user_auth.permissions import (
    DoctorPermission,
    ReciptionPermission,  # Fixed typo in 'ReceptionPermission'
    PharmacyPermission
)

class DoctorReservationAPIView(generics.ListAPIView):
    serializer_class = ReservationSerializer
    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return Reservation.objects.filter(doctorID_id=doctor_id)

class DoctorList(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = doctorSerializer
    def get_permissions(self):
        permission_classes = [IsAdminUser |ReciptionPermission] if self.request.method == "GET" else [IsAdminUser]
        return [permission() for permission in permission_classes]

class DoctorDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = doctorSerializer
    permission_classes = [IsAdminUser |ReciptionPermission]

class ManagementList(generics.ListCreateAPIView):
    queryset = Management.objects.all()
    serializer_class = ManagmentSerializer
    permission_classes = [IsAdminUser]

class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    def get_permissions(self):
        permission_classes = [IsAdminUser |ReciptionPermission] if self.request.method == "GET" else [IsAdminUser]
        return [permission() for permission in permission_classes]

class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminUser |ReciptionPermission]

class PharmacyList(generics.ListCreateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer
    def get(self, request):
        if request.user.role != 2:
            return Response({
                'success': False,
                'status_code': status.HTTP_403_FORBIDDEN,
                'message': 'You are not authorized to perform this action'
            }, status=status.HTTP_403_FORBIDDEN)
        pharmacy = Pharmacy.objects.all()
        serializer = self.get_serializer(pharmacy, many=True)
        return Response({
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'Successfully fetched users',
            'users': serializer.data
        })
class RefoundListCreateAPIView(APIView):
    def get(self, request):
        refounds = Refound.objects.all()
        serializer = RefoundSerializer(refounds, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RefoundSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReceptionListCreateAPIView(APIView):
    def get(self, request):
        receptions = Reception.objects.all()
        serializer = ReceptionSerializer(receptions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReceptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:  
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SpecialtyList(generics.ListAPIView):
    queryset = Specialty.objects.all()
    serializer_class = SpecialtySerializer

class DoctorsBySpecialty(generics.ListAPIView):
    serializer_class = doctorSerializer

    def get_queryset(self):
        specialty_id = self.kwargs['specialty_id']
        specialty = get_object_or_404(Specialty, pk=specialty_id)
        return Doctor.objects.filter(specialty=specialty)
