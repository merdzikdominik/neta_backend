from django.urls import path
from knox import views as knox_views
from .views import (SchedulerView,
                    CreateScheduleView,
                    AllDatesView,
                    ClearScheduleView,
                    RegisterAPI,
                    LoginAPI,
                    UserInfoAPI,
                    AllUsersAPI,
                    ChangePasswordView,
                    CreateHolidayRequestView,
                    ListHolidayRequestsView,
                    UserHolidayRequestsView,
                    ApproveHolidayRequestView,
                    RejectHolidayRequestView)

urlpatterns = [
    path('', SchedulerView.as_view()),
    path('add_holiday', CreateScheduleView.as_view(), name='add_holiday'),
    path('all_dates', AllDatesView.as_view(), name='all_dates'),
    path('clear_schedule', ClearScheduleView.as_view(), name='clear_schedule'),
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('user', UserInfoAPI.as_view(), name='user'),
    path('all_users', AllUsersAPI.as_view(), name='all_users'),
    path('password_change', ChangePasswordView.as_view(), name='password_change'),
    path('create_holiday_request', CreateHolidayRequestView.as_view(), name='create_holiday_request'),
    path('list_holiday_requests', ListHolidayRequestsView.as_view(), name='list_holiday_requests'),
    path('user_holiday_requests', UserHolidayRequestsView.as_view(), name='user_holiday_requests'),
    path('approve_holiday_request/<str:pk>', ApproveHolidayRequestView.as_view(), name='approve_holiday_request'),
    path('reject_holiday_request/<str:pk>', RejectHolidayRequestView.as_view(), name='reject_holiday_request'),
]
