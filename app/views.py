from django.shortcuts import render
from django.views import View
from .models import Product, Cart, Customer, OrderedPlaced
from .forms import CustomerRegisterationForm


class ProductView(View):
    def get(self, request):
        topwears = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BW')
        mobiles = Product.objects.filter(category='M')
        laptops = Product.objects.filter(category='L')
        return render(request, 'app/home.html',{'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles, 'laptops':laptops})

class ProductDetailView(View):
    def get(self, request, pk):
      product = Product.objects.get(pk=pk)
      return render(request, 'app/productdetail.html', {'product' : product})

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Vivo' or data == 'Realme':
        mobiles = Product.objects.filter(category='M', brand=data)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})



def add_to_cart(request):
 return render(request, 'app/addtocart.html')

def buy_now(request):
 return render(request, 'app/buynow.html')

def profile(request): 
 return render(request, 'app/profile.html')

def address(request):
 return render(request, 'app/address.html')

def orders(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request):
 return render(request, 'app/mobile.html')

def login(request):
 return render(request, 'app/login.html')

class CustomerRegistrationView(View):
  def get(self, request):
    form = CustomerRegisterationForm()
    return render(request, 'app/customerregistration.html', {'form' : form})
  
  def post(self, request):
    form = CustomerRegisterationForm(request.POST)
    if form.is_valid():
      form.save()
    return render(request, 'app/customerregistration.html', {'form' : form})
def checkout(request):
 return render(request, 'app/checkout.html')
