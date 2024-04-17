from django.contrib.auth.models import User, AnonymousUser
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from rest_framework.generics import ListAPIView
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
from .models import Scheduler, HolidayRequest, CustomUser, HolidayType, Notification, HolidayPlan, DataChangeRequest, HolidayRequestPlan
from .serializers import (SchedulerSerializer,
                          CreateScheduleSerializer,
                          UserSerializer,
                          RegisterSerializer,
                          ChangePasswordSerializer,
                          HolidayRequestSerializer,
                          CustomUserDataSerializer,
                          HolidayTypeSerializer,
                          NotificationSerializer,
                          HolidayRequestPlanSerializer,
                          DataChangeRequestSerializer
                          )
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication
from django.http import Http404


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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        all_dates = Scheduler.objects.all()
        serializer = SchedulerSerializer(all_dates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ClearScheduleView(APIView):
    def delete(self, request, format=None):
        Scheduler.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CreateHolidayPlanRequest(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user

            serializer = HolidayRequestPlanSerializer(data=request.data)

            if serializer.is_valid():
                user_data = request.data.get('user', {})
                user_instance = CustomUser.objects.get(email=user_data.get('email', ''))

                data = {
                    'user': user_instance,
                    'start_date': serializer.validated_data.get("start_date"),
                    'end_date': serializer.validated_data.get("end_date"),
                    'difference_in_days': serializer.validated_data.get("difference_in_days"),
                    'selected_holiday_type': serializer.validated_data.get("selected_holiday_type"),
                    'message': f"Plan urlopu typu {serializer.validated_data.get('selected_holiday_type')} zaczyna się od {serializer.validated_data.get('start_date')} i kończy {serializer.validated_data.get('end_date')}",
                    'approved': False,
                    'color_hex': serializer.validated_data.get("color_hex", "")
                }

                holiday_plan_request = HolidayRequestPlan.objects.create(**data)

                return Response(
                    HolidayRequestPlanSerializer(holiday_plan_request).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except CustomUser.DoesNotExist:
            return Response({"error": "Użytkownik o podanym adresie e-mail nie istnieje."},
                            status=status.HTTP_404_NOT_FOUND)
        except ValidationError as ve:
            return Response({"error": ve.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class HolidayRequestPlansView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        all_dates = HolidayRequestPlan.objects.all()
        serializer = HolidayRequestPlanSerializer(all_dates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            'age': request.data.get('age', ''),
            'employment_start_date': request.data.get('employment_start_date', ''),
            'employment_end_date': request.data.get('employment_end_date', ''),
            'role': request.data.get('role', ''),
            'education': request.data.get('education', ''),
            'correspondence_address': request.data.get('correspondence_address', ''),
            'tax_office': request.data.get('tax_office', ''),
            'annual_settlement_address': request.data.get('annual_settlement_address', ''),
            'nfz_branch': request.data.get('nfz_branch', ''),
            'id_data': request.data.get('id_data', ''),
            'id_given_by': request.data.get('id_given_by', ''),
            'id_date': request.data.get('id_date', ''),
            'mobile_number_permanent_residence': request.data.get('mobile_number_permanent_residence', ''),
            'city_permanent_residence': request.data.get('city_permanent_residence', ''),
            'postal_code_permanent_residence': request.data.get('postal_code_permanent_residence', ''),
            'post_permanent_residence': request.data.get('post_permanent_residence', ''),
            'municipal_commune_permanent_residence': request.data.get('municipal_commune_permanent_residence', ''),
            'voivodeship_permanent_residence': request.data.get('voivodeship_permanent_residence', ''),
            'country_permanent_residence': request.data.get('country_permanent_residence', ''),
            'street_permanent_residence': request.data.get('street_permanent_residence', ''),
            'house_number_permanent_residence': request.data.get('house_number_permanent_residence', ''),
            'flat_number_permanent_residence': request.data.get('flat_number_permanent_residence', ''),
            'mobile_number_second_residence': request.data.get('mobile_number_second_residence', ''),
            'city_second_residence': request.data.get('city_second_residence', ''),
            'postal_code_second_residence': request.data.get('postal_code_second_residence', ''),
            'post_second_residence': request.data.get('post_second_residence', ''),
            'municipal_commune_second_residence': request.data.get('municipal_commune_second_residence', ''),
            'voivodeship_second_residence': request.data.get('voivodeship_second_residence', ''),
            'country_second_residence': request.data.get('country_second_residence', ''),
            'street_second_residence': request.data.get('street_second_residence', ''),
            'house_number_second_residence': request.data.get('house_number_second_residence', ''),
            'flat_number_second_residence': request.data.get('flat_number_second_residence', ''),
            'mobile_number_correspondence': request.data.get('mobile_number_correspondence', ''),
            'city_correspondence': request.data.get('city_correspondence', ''),
            'postal_code_correspondence': request.data.get('postal_code_correspondence', ''),
            'post_correspondence': request.data.get('post_correspondence', ''),
            'municipal_commune_correspondence': request.data.get('municipal_commune_correspondence', ''),
            'voivodeship_correspondence': request.data.get('voivodeship_correspondence', ''),
            'country_correspondence': request.data.get('country_correspondence', ''),
            'street_correspondence': request.data.get('street_correspondence', ''),
            'house_number_correspondence': request.data.get('house_number_correspondence', ''),
            'flat_number_correspondence': request.data.get('flat_number_correspondence', '')
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

class AllUsersAPI(ListAPIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

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
                    'message': f"Urlop typu {serializer.validated_data.get('selected_holiday_type')} zaczyna się od {serializer.validated_data.get('start_date')} i kończy {serializer.validated_data.get('end_date')}",
                    'approved': False,
                    'color_hex': serializer.validated_data.get("color_hex", "")
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

class ApprovedHolidayRequestsView(generics.ListAPIView):
    serializer_class = HolidayRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        approved_requests = HolidayRequest.objects.filter(approved=True)
        return approved_requests


class ApprovedHolidayPlansRequestsView(generics.ListAPIView):
    serializer_class = HolidayRequestPlanSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        approved_requests = HolidayRequestPlan.objects.filter(approved=True)
        return approved_requests


class UserHolidayRequestsView(generics.ListAPIView):
    serializer_class = HolidayRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        print("Current User:", user)
        return HolidayRequest.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class ApproveHolidayRequestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return HolidayRequest.objects.get(pk=pk)
        except HolidayRequest.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        holiday_request = self.get_object(pk)

        if holiday_request.approved:
            return Response({'detail': 'Holiday request already approved.'}, status=status.HTTP_400_BAD_REQUEST)

        holiday_request.approved = True
        holiday_request.save()

        serializer = HolidayRequestSerializer(holiday_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RejectHolidayRequestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return HolidayRequest.objects.get(pk=pk)
        except HolidayRequest.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        holiday_request = self.get_object(pk)

        if not holiday_request.approved:
            return Response({'detail': 'Holiday request already rejected.'}, status=status.HTTP_400_BAD_REQUEST)

        holiday_request.approved = False
        holiday_request.save()

        serializer = HolidayRequestSerializer(holiday_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ApproveHolidayPlanRequestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return HolidayRequestPlan.objects.get(pk=pk)
        except HolidayRequestPlan.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        holiday_request = self.get_object(pk)

        if holiday_request.approved:
            return Response({'detail': 'Holiday request already approved.'}, status=status.HTTP_400_BAD_REQUEST)

        holiday_request.approved = True
        holiday_request.save()

        serializer = HolidayRequestPlanSerializer(holiday_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RejectHolidayRequestPlanView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return HolidayRequestPlan.objects.get(pk=pk)
        except HolidayRequestPlan.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        holiday_request = self.get_object(pk)

        if not holiday_request.approved:
            return Response({'detail': 'Holiday request already rejected.'}, status=status.HTTP_400_BAD_REQUEST)

        holiday_request.approved = False
        holiday_request.save()

        serializer = HolidayRequestSerializer(holiday_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HolidayTypeView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        all_holiday_types = HolidayType.objects.all()
        serializer = HolidayTypeSerializer(all_holiday_types, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = HolidayTypeSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, format=None):
        try:
            holiday_type_id = request.data.get('id')
            holiday_type = HolidayType.objects.get(id=holiday_type_id)
            holiday_type.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except HolidayType.DoesNotExist:
            return Response({"error": "HolidayType not found"}, status=status.HTTP_404_NOT_FOUND)


class NotificationView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = NotificationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        all_notifications = Notification.objects.all()
        serializer = NotificationSerializer(all_notifications, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, format=None):
        Notification.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DataChangeRequestListView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        data_change_requests = DataChangeRequest.objects.all()
        serializer = DataChangeRequestSerializer(data_change_requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateDataChangeRequestView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = DataChangeRequestSerializer(data=request.data)

            if serializer.is_valid():
                user_data = request.data.get('user', {})
                user_instance = CustomUser.objects.get(email=user_data.get('email', ''))

                data = {
                    'user': user_instance,
                    'surname': serializer.validated_data.get("surname"),
                    'city_permanent_residence': serializer.validated_data.get("city_permanent_residence"),
                    'postal_code_permanent_residence': serializer.validated_data.get("postal_code_permanent_residence"),
                    'post_permanent_residence': serializer.validated_data.get("post_permanent_residence"),
                    'municipal_commune_permanent_residence': serializer.validated_data.get(
                        "municipal_commune_permanent_residence"),
                    'voivodeship_permanent_residence': serializer.validated_data.get("voivodeship_permanent_residence"),
                    'country_permanent_residence': serializer.validated_data.get("country_permanent_residence"),
                    'street_permanent_residence': serializer.validated_data.get("street_permanent_residence"),
                    'house_number_permanent_residence': serializer.validated_data.get(
                        "house_number_permanent_residence"),
                    'flat_number_permanent_residence': serializer.validated_data.get("flat_number_permanent_residence"),
                    'mobile_number_permanent_residence': serializer.validated_data.get(
                        "mobile_number_permanent_residence"),
                    'city_second_residence': serializer.validated_data.get("city_second_residence"),
                    'postal_code_second_residence': serializer.validated_data.get("postal_code_second_residence"),
                    'post_second_residence': serializer.validated_data.get("post_second_residence"),
                    'municipal_commune_second_residence': serializer.validated_data.get(
                        "municipal_commune_second_residence"),
                    'voivodeship_second_residence': serializer.validated_data.get("voivodeship_second_residence"),
                    'country_second_residence': serializer.validated_data.get("country_second_residence"),
                    'street_second_residence': serializer.validated_data.get("street_second_residence"),
                    'house_number_second_residence': serializer.validated_data.get("house_number_second_residence"),
                    'flat_number_second_residence': serializer.validated_data.get("flat_number_second_residence"),
                    'mobile_number_second_residence': serializer.validated_data.get("mobile_number_second_residence"),
                    'city_correspondence_residence': serializer.validated_data.get("city_correspondence_residence"),
                    'postal_code_correspondence_residence': serializer.validated_data.get(
                        "postal_code_correspondence_residence"),
                    'post_correspondence_residence': serializer.validated_data.get("post_correspondence_residence"),
                    'municipal_commune_correspondence_residence': serializer.validated_data.get(
                        "municipal_commune_correspondence_residence"),
                    'voivodeship_correspondence_residence': serializer.validated_data.get(
                        "voivodeship_correspondence_residence"),
                    'country_correspondence_residence': serializer.validated_data.get(
                        "country_correspondence_residence"),
                    'street_correspondence_residence': serializer.validated_data.get("street_correspondence_residence"),
                    'house_number_correspondence_residence': serializer.validated_data.get(
                        "house_number_correspondence_residence"),
                    'flat_number_correspondence_residence': serializer.validated_data.get(
                        "flat_number_correspondence_residence"),
                    'mobile_number_correspondence_residence': serializer.validated_data.get(
                        "mobile_number_correspondence_residence"),
                    'correspondence_address': serializer.validated_data.get("correspondence_address"),
                    'tax_office': serializer.validated_data.get("tax_office"),
                    'annual_settlement_address': serializer.validated_data.get("annual_settlement_address"),
                    'nfz_branch': serializer.validated_data.get("nfz_branch"),
                    'id_data': serializer.validated_data.get("id_data"),
                    'id_given_by': serializer.validated_data.get("id_given_by"),
                    'id_date': serializer.validated_data.get("id_date"),
                    'approved': False,
                }

                data_change_request = DataChangeRequest.objects.create(**data)

                return Response(
                    DataChangeRequestSerializer(data_change_request).data,
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


class ApprovedDataChangeRequestsView(generics.ListAPIView):
    serializer_class = DataChangeRequestSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        approved_requests = DataChangeRequest.objects.filter(approved=True)
        return approved_requests


class ApproveDataChangeRequestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return DataChangeRequest.objects.get(pk=pk)
        except DataChangeRequest.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated]
        data_change_request = self.get_object(pk)

        if data_change_request.approved:
            return Response({'detail': 'Holiday request already approved.'}, status=status.HTTP_400_BAD_REQUEST)

        data_change_request.approved = True
        data_change_request.save()

        serializer = DataChangeRequestSerializer(data_change_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RejectDataChangeRequestView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get_object(self, pk):
        try:
            return DataChangeRequest.objects.get(pk=pk)
        except DataChangeRequest.DoesNotExist:
            raise Http404

    def patch(self, request, pk):
        data_change_request = self.get_object(pk)

        if not data_change_request.approved:
            return Response({'detail': 'Holiday request already rejected.'}, status=status.HTTP_400_BAD_REQUEST)

        data_change_request.approved = False
        data_change_request.save()

        serializer = DataChangeRequestSerializer(data_change_request)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateUserDataView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        approved_requests = DataChangeRequest.objects.filter(approved=True)

        for notification in approved_requests:
            user_email = notification.user.email
            try:
                user = CustomUser.objects.get(email=user_email)

                if notification.surname:
                    user.last_name = notification.surname
                if notification.city_permanent_residence:
                    user.city_permanent_residence = notification.city_permanent_residence
                if notification.postal_code_permanent_residence:
                    user.postal_code_permanent_residence = notification.postal_code_permanent_residence
                if notification.post_permanent_residence:
                    user.post_permanent_residence = notification.post_permanent_residence
                if notification.municipal_commune_permanent_residence:
                    user.municipal_commune_permanent_residence = notification.municipal_commune_permanent_residence
                if notification.voivodeship_permanent_residence:
                    user.voivodeship_permanent_residence = notification.voivodeship_permanent_residence
                if notification.country_permanent_residence:
                    user.country_permanent_residence = notification.country_permanent_residence
                if notification.street_permanent_residence:
                    user.street_permanent_residence = notification.street_permanent_residence
                if notification.house_number_permanent_residence:
                    user.house_number_permanent_residence = notification.house_number_permanent_residence
                if notification.flat_number_permanent_residence:
                    user.flat_number_permanent_residence = notification.flat_number_permanent_residence
                if notification.mobile_number_permanent_residence:
                    user.mobile_number_permanent_residence = notification.mobile_number_permanent_residence

                if notification.city_second_residence:
                    user.city_second_residence = notification.city_second_residence
                if notification.postal_code_second_residence:
                    user.postal_code_second_residence = notification.postal_code_second_residence
                if notification.post_second_residence:
                    user.post_second_residence = notification.post_second_residence
                if notification.municipal_commune_second_residence:
                    user.municipal_commune_second_residence = notification.municipal_commune_second_residence
                if notification.voivodeship_second_residence:
                    user.voivodeship_second_residence = notification.voivodeship_second_residence
                if notification.country_second_residence:
                    user.country_second_residence = notification.country_second_residence
                if notification.street_second_residence:
                    user.street_second_residence = notification.street_second_residence
                if notification.house_number_second_residence:
                    user.house_number_second_residence = notification.house_number_second_residence
                if notification.flat_number_second_residence:
                    user.flat_number_second_residence = notification.flat_number_second_residence
                if notification.mobile_number_second_residence:
                    user.mobile_number_second_residence = notification.mobile_number_second_residence

                if notification.city_correspondence_residence:
                    user.city_correspondence = notification.city_correspondence_residence
                if notification.postal_code_correspondence_residence:
                    user.postal_code_correspondence = notification.postal_code_correspondence_residence
                if notification.post_correspondence_residence:
                    user.post_correspondence = notification.post_correspondence_residence
                if notification.municipal_commune_correspondence_residence:
                    user.municipal_commune_correspondence = notification.municipal_commune_correspondence_residence
                if notification.voivodeship_correspondence_residence:
                    user.voivodeship_correspondence = notification.voivodeship_correspondence_residence
                if notification.country_correspondence_residence:
                    user.country_correspondence = notification.country_correspondence_residence
                if notification.street_correspondence_residence:
                    user.street_correspondence = notification.street_correspondence_residence
                if notification.house_number_correspondence_residence:
                    user.house_number_correspondence = notification.house_number_correspondence_residence
                if notification.flat_number_correspondence_residence:
                    user.flat_number_correspondence = notification.flat_number_correspondence_residence
                if notification.mobile_number_correspondence_residence:
                    user.mobile_number_correspondence = notification.mobile_number_correspondence_residence

                if notification.tax_office:
                    user.tax_office = notification.tax_office
                if notification.correspondence_address:
                    user.correspondence_address = notification.correspondence_address
                if notification.annual_settlement_address:
                    user.annual_settlement_address = notification.annual_settlement_address
                if notification.nfz_branch:
                    user.nfz_branch = notification.nfz_branch
                if notification.id_data:
                    user.id_data = notification.id_data
                if notification.id_given_by:
                    user.id_given_by = notification.id_given_by
                if notification.id_date:
                    user.id_date = notification.id_date
            except CustomUser.DoesNotExist:
                continue

            user.save()

        return Response({'success': True})
