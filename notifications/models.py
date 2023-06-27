from django.db import models
from accounts.models import User

# Create your models here.
Categories = (
    ("Lost spot", "Lost spot"),
    ("Winner", "Winner"),
    ("Completed", "Completed"),
    ("Debit","Debit"),
    ("Credit","Credit"),
)

class NotificationCategory(models.Model):
    image = models.ImageField(upload_to='notifications/')
    category = models.CharField(max_length=100,unique=True,choices=Categories)

    def __str__(self):
        return f"{self.category}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.ForeignKey(NotificationCategory, on_delete=models.CASCADE, default="")
    text = models.CharField(max_length=300)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}"
