from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets
from django.shortcuts import render
from .serializers import *
from base_app.permissions import *
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from patient.views import gen_context


def registration(request):
    return render(request, 'page-register.html')


def edit_role(request, *args, **kwargs):
    return render(request, 'edit_role.html', gen_context(request))


class UserAPIView(viewsets.ModelViewSet):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated&IsBoss]
    queryset=User.objects.all()

    def get_serializer_class(self):
        serializer_class = ProfileSerializer
        if self.request.method == 'POST':
            serializer_class = CreateUserSerializer
        elif self.request.method == 'PUT' or self.request.method == 'PATCH':
            serializer_class = RoleEditSerializer
        return serializer_class

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN)


class PasswordChangeAPIView(generics.UpdateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = PasswordSerializer

    def get_object(self):
        return self.request.user


class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


