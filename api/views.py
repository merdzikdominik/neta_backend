from django.contrib.auth.models import User, AnonymousUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from rest_framework.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import login, get_user_model
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import status, generics, permissions
from rest_framework.permissions import IsAuthenticated
from knox.views import APIView as KnoxApiView
from .models import Scheduler, HolidayRequest, CustomUser
from .serializers import (SchedulerSerializer,
                          CreateScheduleSerializer,
                          UserSerializer,
                          RegisterSerializer,
                          ChangePasswordSerializer,
                          HolidayRequestSerializer,
                          CustomUserDataSerializer
                          )
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication


class SchedulerView(generics.ListAPIView):
    queryset = Scheduler.objects.all()
    serializer_class = SchedulerSerializer
@method_decorator(csrf_exempt, name='dispatch')
class CreateScheduleView(APIView):
    serializer_class = CreateScheduleSerializer

    def post(self, request, format=None):
        host = request.session.session_key

        if not host:
            request.session.create()
            host = request.session.session_key

        mutable_data = request.data.copy()
        mutable_data['host'] = host

        serializer = self.serializer_class(data=mutable_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)

class AllDatesView(APIView):
    def get(self, request, format=None):
        all_dates = Scheduler.objects.all()
        serializer = SchedulerSerializer(all_dates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClearScheduleView(APIView):
    def delete(self, request, format=None):
        Scheduler.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = {
            'email': serializer.validated_data['email'],
            'password': serializer.validated_data['password'],
            'first_name': request.data.get('first_name', ''),
            'second_name': request.data.get('second_name', ''),
            'last_name': request.data.get('last_name', ''),
            'birth_date': request.data.get('birth_date', ''),
            'mobile_number': request.data.get('mobile_number', ''),
            'age': request.data.get('age', ''),
            'employment_start_date': request.data.get('employment_start_date', ''),
            'employment_end_date': request.data.get('employment_end_date', ''),
            'role': request.data.get('role', ''),
            'education': request.data.get('education', '')
        }

        user = serializer.create(validated_data)

        return Response({
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })

class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']

        login(request, user)

        token = AuthToken.objects.create(user)
        if token:
            response_data = {
                'user': UserSerializer(user, context=self).data,
                'is_superuser': user.is_superuser,
                'token': token[1],
            }
        else:
            response_data = {
                'user': UserSerializer(user, context=self).data,
                'is_superuser': user.is_superuser,
            }

        return Response(response_data)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = request.user
            old_password = serializer.validated_data.get("old_password")
            new_password = serializer.validated_data.get("new_password")

            if not user.check_password(old_password):
                return Response({"detail": "Stare hasło jest niepoprawne."}, status=status.HTTP_400_BAD_REQUEST)

            if not old_password and not new_password:
                return Response({'error': 'Podaj stare i nowe hasło.'}, status=status.HTTP_400_BAD_REQUEST)

            if not old_password and new_password:
                return Response({'error': 'Wykryto tylko podane nowe hasło, podaj też obecne.'}, status=status.HTTP_400_BAD_REQUEST)

            if old_password == new_password:
                return Response({"detail": "Nowe hasło nie może być takie samo jak stare hasło."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"detail": "Hasło zostało pomyślnie zmienione."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserInfoAPI(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateHolidayRequestView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user

            serializer = HolidayRequestSerializer(data=request.data)

            if serializer.is_valid():
                user_data = request.data.get('user', {})
                user_instance = CustomUser.objects.get(email=user_data.get('email', ''))

                data = {
                    'user': user_instance,
                    'start_date': serializer.validated_data.get("start_date"),
                    'end_date': serializer.validated_data.get("end_date"),
                    'difference_in_days': serializer.validated_data.get("difference_in_days"),
                    'selected_holiday_type': serializer.validated_data.get("selected_holiday_type"),
                    'message': f"Urlop zaczyna się od {serializer.validated_data.get('start_date')} i kończy {serializer.validated_data.get('end_date')}, typ urlopu: {serializer.validated_data.get('selected_holiday_type')}",
                    'approved': False
                }

                holiday_request = HolidayRequest.objects.create(**data)

                return Response(
                    HolidayRequestSerializer(holiday_request).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({"error": "Użytkownik o podanym adresie e-mail nie istnieje."}, status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListHolidayRequestsView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        holiday_requests = HolidayRequest.objects.all()
        serializer = HolidayRequestSerializer(holiday_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
