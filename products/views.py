from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Products, Bidding, ProductCategory
from .forms import AddProductForm
from django.utils import timezone
import datetime
from accounts.models import User
from wallet.models import Wallet
from notifications.models import Notification, NotificationCategory
from decimal import Decimal
from django.urls import reverse_lazy,reverse
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.forms import ValidationError
        
class AllCategoriesView(ListView):
    model = ProductCategory
    template_name = 'all_categories.html'
    context_object_name = 'categories'

class CategoryDetailView(View):
    def get(self, request, id):
        category = ProductCategory.objects.get(id=id)
        products = Products.objects.filter(category=category)
        print(category,category.category)

        context = {
            'category': category,
            'products': products,
        }
        return render(request, 'category_detail.html', context)

class LiveProductsListView(ListView):
    model = Products
    template_name = 'live_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        Products.objects.filter(deadline__lt=timezone.now().date()).update(is_live=False)
        return Products.objects.filter(is_live=True)

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Products
    template_name = 'product_detail.html'
    context_object_name = 'product'
    login_url = '/accounts/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class AddProductView(LoginRequiredMixin, CreateView):
    model = Products
    form_class = AddProductForm
    template_name = 'add_product.html'
    success_url = '/products/myproducts/'

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)

class UserProductsView(LoginRequiredMixin, ListView):
    model = Products
    template_name = 'my_products.html'
    context_object_name = 'my_products'

    def get_queryset(self):
        Products.objects.filter(deadline__lt=timezone.now().date()).update(is_live=False)
        return Products.objects.filter(seller=self.request.user)

class BiddingListView(LoginRequiredMixin, ListView):
    model = Bidding
    template_name = 'bidding_list.html'
    login_url = '/accounts/login/'

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        queryset = super().get_queryset().filter(product_id=product_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs.get('product_id')
        user = self.request.user
        queryset = context['object_list']
        res = Bidding.objects.filter(product_id=product_id,user=user)
        prod = Products.objects.get(id=product_id)
        owner = prod.seller
        base = min(prod.base_price,5000)
        if res:
            result = 'No'
        else:
            result = 'Yes'

        if prod.deadline > timezone.now().date():
            dead = 'No'
        else:
            dead = 'Yes'
        context['result'] = result
        context['base'] = base
        context['theid'] = product_id
        context['now'] = dead
        context['user'] = user
        context['owner'] = owner

        return context

class ConfirmParticipationView(View):
    def get(self, request, product_id):
        product = Products.objects.get(id=product_id)
        base_price = min(product.base_price,5000)

        context = {
            'product_id': product_id,
            'amount': base_price,
        }
        return render(request, 'confirm_participation.html', context)

class ConfirmView(View):
    def get(self, request, product_id):
        product = Products.objects.get(id=product_id)
        base_price = min(product.base_price,5000)
        base_priced = Decimal(base_price)
        user = request.user
        wallet = Wallet.objects.get(user=user)
        if wallet.balance < base_price:
            return redirect('products:no_balance')
        wallet.balance -= base_priced
        wallet.save()

        Bidding.objects.create(user=user,product=product,amount=base_price,is_verified='True')

        category = NotificationCategory.objects.get(category='Debit')
        text = f"An amount of ₹{base_priced} has been debited from your wallet."
        notify = Notification.objects.create(user=user,type=category,text=text)

        return redirect(reverse('products:product_bids', kwargs={ 'product_id': product_id }))

class NoBalanceView(TemplateView):
    template_name = 'insufficient_balance.html'

class NoBasePrizeView(TemplateView):
    template_name = 'base_error.html'

class NoHighBidView(TemplateView):
    template_name = 'high_error.html'

class BidAgainView(LoginRequiredMixin, CreateView):
    model = Bidding
    fields = ['amount']
    template_name = 'bid_again.html'

    def get_success_url(self):
        return reverse_lazy('products:product_bids', kwargs={'product_id': self.kwargs['product_id']})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.product_id = self.kwargs['product_id']
        amount = form.cleaned_data['amount']
        product = Products.objects.get(pk=self.kwargs['product_id'])
        if product.base_price >= amount:
            return redirect("products:base_error")
        now = timezone.now().date()
        if product.deadline != now:
            if amount > product.highest_bid:
                old_amount = product.highest_bid
                if old_amount != Decimal(0):
                    old_bid = Bidding.objects.filter(amount=old_amount).first()
                    old_winner = User.objects.get(username=old_bid.user)
                    category = NotificationCategory.objects.get(category='Lost spot')
                    text = f"You are no more the highest bidder for the product {product.name}! Bid again to reclaim!"
                    notify = Notification.objects.create(user=old_winner,type=category,text=text)
                product.highest_bid = amount
                product.save()
                return super().form_valid(form)
            else:
                return redirect("products:high_error")
        else:
            if amount > product.highest_bid:
                product.highest_bid = amount
                product.save()
            else:
                product.save()
            return super().form_valid(form)
        # if amount > product.highest_bid:
        #     now = timezone.now().date()
        #     print(product.deadline,now)
        #     if product.deadline != now:
        #         print(product.deadline,now)
        #         product.highest_bid = amount
        #         product.save()
        #     return super().form_valid(form)
        # else:
        #     return redirect("products:high_error")

class EndBiddingView(View):
    def get(self, request, product_id):
        product = Products.objects.get(id=product_id)
        product.is_live = False
        product.save()
        base = min(product.base_price, 5000)
        biddings = Bidding.objects.filter(product=product,amount=base)
        print(product,biddings)

        # Add amount to users' wallets
        for bidding in biddings:
            user = bidding.user
            wallet = Wallet.objects.get(user=user)
            amount = min(Decimal(product.base_price), 5000)
            print(user,wallet,amount,wallet.balance)
            wallet.balance += amount
            print(wallet.balance)
            wallet.save()
            category = NotificationCategory.objects.get(category='Credit')
            text = f"An amount of ₹{amount} has been credited to your wallet."
            notify = Notification.objects.create(user=user,type=category,text=text)
            category = NotificationCategory.objects.get(category='Completed')
            text = f"The auction process for product {product.name} has completed."
            notify = Notification.objects.create(user=user,type=category,text=text)

        winning_bid = Bidding.objects.get(amount=product.highest_bid)
        winner = User.objects.get(username=winning_bid.user)
        print(winning_bid,winner)
        category = NotificationCategory.objects.get(category='Winner')
        text = f"Congratulations! You are the winner for the product {product.name}!"
        notify = Notification.objects.create(user=winner,type=category,text=text)
        return redirect('products:product_detail', pk=product_id)

class HighestBidderView(View):
    def get(self, request, product_id):
        product = Products.objects.get(id=product_id)
        if not product.is_live:
            bid = Bidding.objects.get(amount=product.highest_bid)
            user = User.objects.get(username=bid.user)
            context = {
                'username': user.username,
                'name': user.first_name+' '+user.last_name,
                'mobile_no': user.mobile_no,
                'email': user.email,
                'pincode': user.pincode,
            }
            return render(request, 'winner.html', context)
        else:
            return render(request, 'wait.html')
