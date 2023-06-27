from django.shortcuts import render
from .models import Notification
from django.views import View

# Create your views here.
class UserNotifications(View):
    def get(self, request):
        user = request.user
        notifications = Notification.objects.filter(user=user).order_by('-time')

        context = {
            'notifications': notifications,
        }
        return render(request, 'notifications.html', context)
