from django.urls import path
from knox import views as knox_views
from .views import SchedulerView, \
    CreateScheduleView, \
    AllDatesView, \
    ClearScheduleView, \
    RegisterAPI, \
    LoginAPI, \
    UserInfoAPI

urlpatterns = [
    path('', SchedulerView.as_view()),
    path('add_holiday', CreateScheduleView.as_view(), name='add_holiday'),
    path('all_dates', AllDatesView.as_view(), name='all_dates'),
    path('clear_schedule', ClearScheduleView.as_view(), name='clear_schedule'),
    path('register', RegisterAPI.as_view(), name='register'),
    path('login', LoginAPI.as_view(), name='login'),
    path('logout', knox_views.LogoutView.as_view(), name='logout'),
    path('user_info', UserInfoAPI.as_view(), name='user_info')
]



