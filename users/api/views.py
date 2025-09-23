from rest_framework import generics, permissions
from .serializers import UserSignupSerializer, LibrarianSignupSerializer

class UserSignupView(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

class LibrarianSignupView(generics.CreateAPIView):
    serializer_class = LibrarianSignupSerializer
    permission_classes = [permissions.IsAdminUser]
