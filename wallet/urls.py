from django.urls import path
from . import views

app_name = 'wallet'

urlpatterns = [
    path('balance/', views.WalletBalanceView.as_view(), name='balance'),
    path('addfunds/', views.AddFundsView.as_view(), name='add_funds'),
]
