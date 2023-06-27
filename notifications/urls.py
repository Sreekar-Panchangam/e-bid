from django.urls import path
from .views import *

app_name = 'notifications'

urlpatterns = [
    path('', UserNotifications.as_view(), name='notifications'),
]
