from django.views.generic import TemplateView
from products.models import Products, ProductCategory
from django.utils import timezone

class ThanksPage(TemplateView):
    template_name = 'thanks.html'

class HomePage(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        live_products = Products.objects.filter(is_live=True)[:6]
        categories = ProductCategory.objects.all()[:7]
        closed_products = Products.objects.filter(is_live=False).order_by('-deadline')[:9]

        context['live_products'] = live_products
        context['closed_products'] = closed_products
        context['categories'] = categories
        return context

class ConfirmSignUpView(TemplateView):
    template_name = 'confirm.html'
