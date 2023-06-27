from django.urls import path
from .views import *

app_name = 'products'

urlpatterns = [
    path('categories/', AllCategoriesView.as_view(), name='all_categories'),
    path('categories/<int:id>/', CategoryDetailView.as_view(), name='category_detail'),
    path('liveproducts/', LiveProductsListView.as_view(), name='live_products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/add/', AddProductView.as_view(), name='add_product'),
    path('myproducts/', UserProductsView.as_view(), name='my_products'),
    path('product/<int:product_id>/biddings/', BiddingListView.as_view(), name='product_bids'),
    path('product/<int:product_id>/participation/', ConfirmParticipationView.as_view(), name='confirm_participation'),
    path('product/<int:product_id>/bidagain/', BidAgainView.as_view(), name='bid_again'),
    path('product/<int:product_id>/confirm/', ConfirmView.as_view(), name='confirm'),
    path('product/<int:product_id>/end/', EndBiddingView.as_view(), name='end_bidding'),
    path('product/<int:product_id>/winner/', HighestBidderView.as_view(), name='winner'),
    path('nobalance/', NoBalanceView.as_view(), name='no_balance'),
    path('berror/', NoBasePrizeView.as_view(), name='base_error'),
    path('herror/', NoHighBidView.as_view(), name='high_error'),
]
