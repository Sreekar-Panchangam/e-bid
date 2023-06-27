from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import FormView
from .forms import AddFundsForm
from decimal import Decimal

class WalletBalanceView(LoginRequiredMixin, TemplateView):
    template_name = 'wallet_balance.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        wallet = user.wallet  # Assuming the wallet is related to the User model through a OneToOneField or ForeignKey
        context['balance'] = wallet.balance
        return context

class AddFundsView(LoginRequiredMixin, FormView):
    template_name = 'add_funds.html'
    form_class = AddFundsForm
    success_url = '/wallet/balance/'  # Redirect to the wallet balance page

    def form_valid(self, form):
        amount = Decimal(form.cleaned_data['amount'])
        user = self.request.user
        wallet = user.wallet
        wallet.balance += amount
        wallet.save()
        return super().form_valid(form)
