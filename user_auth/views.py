from rest_framework import generics, response, status
from user_auth.models import DoctorProfile, PatientProfile
from .serializers import DoctorRegistrationSerializer, PatientRegistrationSerializer, LoginSerializer

class DoctorRegisterView(generics.CreateAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorRegistrationSerializer

class PatientRegisterView(generics.CreateAPIView):
    queryset = PatientProfile.objects.all()
    serializer_class = PatientRegistrationSerializer

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return response.Response({
            "user": user.username,
            "token": user.auth_token.key
        }, status=status.HTTP_200_OK)



# Logout View - Uncomment and ensure it uses the correct serializer
#class LogoutAPIView(generics.GenericAPIView):
   # serializer_class = LoginSerializer
   # permission_classes = (IsAuthenticated,)
  #  def post(self, request):
       # serializer = self.serializer_class(data=request.data)
       # serializer.is_valid(raise_exception=True)
      #  serializer.save()
        #return Response(status=status.HTTP_204_NO_CONTENT)


# class LogoutAPIView(generics.GenericAPIView):
#     serializer_class = LogoutSerializer
#     permission_classes = (IsAuthenticated,)
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(status=status.HTTP_204_NO_CONTENT)