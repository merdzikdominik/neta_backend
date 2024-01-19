from django.urls import path
from .views import SchedulerView, CreateScheduleView

urlpatterns = [
    path('', SchedulerView.as_view()),
    path('add_holiday', CreateScheduleView.as_view(), name='add_holiday')
]
