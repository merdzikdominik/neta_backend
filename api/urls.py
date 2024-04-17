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
                    CreateHolidayPlanRequest,
                    HolidayRequestPlansView,
                    ListHolidayRequestsView,
                    UserHolidayRequestsView,
                    ApproveHolidayRequestView,
                    RejectHolidayRequestView,
                    ApproveHolidayPlanRequestView,
                    RejectHolidayRequestPlanView,
                    HolidayTypeView,
                    NotificationView,
                    CreateHolidayRequestView,
                    ApprovedHolidayRequestsView,
                    ApprovedHolidayPlansRequestsView,
                    DataChangeRequestListView,
                    CreateDataChangeRequestView,
                    ApproveDataChangeRequestView,
                    RejectDataChangeRequestView,
                    ApprovedDataChangeRequestsView,
                    UpdateUserDataView)

urlpatterns = [
    path('', SchedulerView.as_view()),
    path('add_holiday', CreateScheduleView.as_view(), name='add_holiday'),
    path('all_dates', AllDatesView.as_view(), name='all_dates'),
    path('clear_schedule', ClearScheduleView.as_view(), name='clear_schedule'),
    path('all_holiday_plans', HolidayRequestPlansView.as_view(), name='all_holiday_plans'),
    path('create_holiday_plan_request', CreateHolidayPlanRequest.as_view(), name='create_holiday_plan_request'),
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('user', UserInfoAPI.as_view(), name='user'),
    path('all_users', AllUsersAPI.as_view(), name='all_users'),
    path('password_change', ChangePasswordView.as_view(), name='password_change'),
    path('create_holiday_request', CreateHolidayRequestView.as_view(), name='create_holiday_request'),
    path('list_holiday_requests', ListHolidayRequestsView.as_view(), name='list_holiday_requests'),
    path('list_holiday_approved_requests', ApprovedHolidayRequestsView.as_view(), name='list_holiday_approved_requests'),
    path('list_holiday_approved_requests_plans', ApprovedHolidayPlansRequestsView.as_view(), name='list_holiday_approved_requests_plans'),
    path('user_holiday_requests', UserHolidayRequestsView.as_view(), name='user_holiday_requests'),
    path('approve_holiday_request/<str:pk>', ApproveHolidayRequestView.as_view(), name='approve_holiday_request'),
    path('reject_holiday_request/<str:pk>', RejectHolidayRequestView.as_view(), name='reject_holiday_request'),
    path('approve_holiday_plan_request/<str:pk>', ApproveHolidayPlanRequestView.as_view(), name='approve_holiday_request_plan'),
    path('reject_holiday_plan_request/<str:pk>', RejectHolidayRequestPlanView.as_view(), name='reject_holiday_request_plan'),
    path('all_holiday_types', HolidayTypeView.as_view(), name='all_holiday_types'),
    path('all_notifications', NotificationView.as_view(), name='all_notifications'),
    path('all_data_change_requests', DataChangeRequestListView.as_view(), name='all_data_change_requests'),
    path('all_approved_data_change_requests', ApprovedDataChangeRequestsView.as_view(), name='all_approved_data_change_requests'),
    path('create_data_change_request', CreateDataChangeRequestView.as_view(), name='create_data_change_request'),
    path('approve_data_change_request/<str:pk>', ApproveDataChangeRequestView.as_view(), name='approve_data_change_request'),
    path('reject_data_change_request/<str:pk>', RejectDataChangeRequestView.as_view(), name='reject_data_change_request'),
    path('update_user_data', UpdateUserDataView.as_view(), name='update_user_data')
]