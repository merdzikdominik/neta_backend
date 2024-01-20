from django.urls import path
from .views import SchedulerView, CreateScheduleView, AllDatesView, ClearScheduleView, RegisterAPI

urlpatterns = [
    path('', SchedulerView.as_view()),
    path('add_holiday', CreateScheduleView.as_view(), name='add_holiday'),
    path('all_dates', AllDatesView.as_view(), name='all_dates'),
    path('clear_schedule', ClearScheduleView.as_view(), name='clear_schedule'),
    path('register', RegisterAPI.as_view(), name='register')
]
