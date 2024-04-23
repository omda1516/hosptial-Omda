# in models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class HospitalUser(AbstractUser):
    GENDERS = [
        ("male", "Male"),
        ("female", "Female"),
    ]
    gender = models.CharField(choices=GENDERS, max_length=20)


    def in_group(self, group_name : str):
        """This is a method to check if a user is belong to a specific group."""
        return self.request.user.groups.filter(name=group_name).exists()
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }



# class User(AbstractUser):
  
#   # These fields tie to the roles!
#     ADMIN = 1
#     STAFF = 2
#     USER = 3

#     ROLE_CHOICES = (
#         (ADMIN, 'Admin'),
#         (STAFF, 'STAFF'),
#         (USER, 'USER')
#     )

#     class Meta:
#         verbose_name = 'user'
#         verbose_name_plural = 'users'
#     # Roles created here
#     uid = models.UUIDField(unique=True, editable=False, default=uuid.uuid4, verbose_name='Public identifier')
#     username=models.CharField(max_length=40,unique=True)
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=30, blank=True)
#     phone_number = models.CharField(max_length=15,null=True)
#     pin = models.IntegerField(null=True)  # Adjust max_digits as per your requirement
#     role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True, default=3)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     is_active = models.BooleanField(default=True)
#     is_deleted = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=True)
#     is_superuser = models.BooleanField(default=True)
#     created_date = models.DateTimeField(default=timezone.now)
#     modified_date = models.DateTimeField(default=timezone.now)
#     created_by = models.EmailField()
#     modified_by = models.EmailField()


#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']


#     def __str__(self):
#             return self.email
    
    
#     def in_group(self, group_name : str):
#         """This is a method to check if a user is belong to a specific group."""
#         return self.request.user.groups.filter(name=group_name).exists()
