from django.shortcuts import render, redirect
from django.views import View
from .models import Product, Cart, Customer, OrderedPlaced
from .forms import CustomerRegisterationForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required # for function based view
from django.utils.decorators import method_decorator # for class based view

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
      item_already_in_cart = False
      item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
      return render(request, 'app/productdetail.html', {'product' : product, 'item_already_in_cart' : item_already_in_cart})
    
class CustomerRegistrationView(View):
  def get(self, request):
    form = CustomerRegisterationForm()
    return render(request, 'app/customerregistration.html', {'form' : form})
  
  def post(self, request):
    form = CustomerRegisterationForm(request.POST)
    if form.is_valid():
      messages.success(request, 'Congratulations! You registered sucessfully.')
      form.save()
    return render(request, 'app/customerregistration.html', {'form' : form})

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Vivo' or data == 'Realme':
        mobiles = Product.objects.filter(category='M', brand=data)
    return render(request, 'app/mobile.html', {'mobiles': mobiles})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
  def get(self, request):
    form = CustomerProfileForm()
    return render(request, 'app/profile.html', {'form' : form, 'active' :'btn-primary'})

  def post(self, request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
      current_user = request.user
      name = form.cleaned_data['name']
      locality = form.cleaned_data['locality']
      city = form.cleaned_data['city']
      state = form.cleaned_data['state']
      zipcode = form.cleaned_data['zipcode']
      customer_address_form = Customer(user = current_user, name = name, locality = locality, city = city, state = state, zipcode = zipcode)
      customer_address_form.save()
      messages.success(request, 'Your profile updated successfully!')
    return render(request, 'app/profile.html', {'form' : form, 'active' : 'btn-primary'})

@login_required
def add_to_cart(request):
  user = request.user
  product_id = request.GET.get('prod_id')
  product = Product.objects.get(id = product_id)
  Cart(user=user, product = product).save()
  return redirect('/cart')

@login_required
def show_cart(request):
  if request.user.is_authenticated:
    user = request.user
    cart = Cart.objects.filter(user = user)
    print(cart)
    amount = 0.0
    shipping_amount = 0.0
    total_amount = 0.0
    cart_product = [product for product in Cart.objects.all() if product.user == user]
    if cart_product:
      for product in cart_product:
        tempamount = (product.quantity * product.product.discount_price)
        amount += tempamount
        if amount > 500:
          shipping_amount = 70.0
        else:
          shipping_amount = 0.0
        total_amount = amount + shipping_amount
      return render(request, 'app/addtocart.html', {'carts' : cart, 'total_amount':total_amount, 'amount' : amount, 'shipping_amount' : shipping_amount})
    else:
      return render(request, 'app/emptycart.html')

def plus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    # in cart get one object(that's we using get) which product id we have in prod_id and this product must be of loginned user
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    user = request.user
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [product for product in Cart.objects.all() if product.user == user]
    for product in cart_product:
      tempamount = (product.quantity * product.product.discount_price)
      amount += tempamount
      if amount > 500:
        shipping_amount = 70.0
      else:
        shipping_amount = 0.0
      total_amount = amount + shipping_amount
    data = {
      'quantity' : c.quantity,
      'amount' : amount,
      'shippingamount' : shipping_amount,
      'totalamount' : total_amount
    }
    return JsonResponse(data)
  
def minus_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    # in cart get one object(that's we using get) which product id we have in prod_id and this product must be of loginned user
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity-=1
    c.save()
    user = request.user
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [product for product in Cart.objects.all() if product.user == user]
    for product in cart_product:
      tempamount = (product.quantity * product.product.discount_price)
      amount += tempamount
      total_amount = amount + shipping_amount
    data = {
      'quantity' : c.quantity,
      'amount' : amount,
      'shippingamount' : shipping_amount,
      'totalamount' : total_amount
    }
    return JsonResponse(data)


def remove_cart(request):
  if request.method == 'GET':
    prod_id = request.GET['prod_id']
    # in cart get one object(that's we using get) which product id we have in prod_id and this product must be of loginned user
    c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.delete()
    user = request.user
    amount = 0.0
    shipping_amount = 70.0
    cart_product = [product for product in Cart.objects.all() if product.user == user]
    for product in cart_product:
      tempamount = (product.quantity * product.product.discount_price)
      amount += tempamount
      total_amount = amount + shipping_amount
    data = {
      'amount' : amount,
      'totalamount' : total_amount
    }
    return JsonResponse(data)


def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 current_user_address = Customer.objects.filter(user = request.user)
 return render(request, 'app/address.html', {'current_user_address' : current_user_address, 'active' : 'btn-primary'})

@login_required
def orders(request):
  op = OrderedPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html', {'order_placed' : op})

def mobile(request):
 return render(request, 'app/mobile.html')


@login_required
def checkout(request):
  user = request.user
  add = Customer.objects.filter(user = user)
  cart_item = Cart.objects.filter(user = user)
  amount = 0.0
  shipping_amount = 70.0
  totalamount = 0.0
  cart_product = [product for product in Cart.objects.all() if product.user == user]
  
  if cart_product:
    for product in cart_product:
      tempamount = (product.quantity * product.product.discount_price)
      amount += tempamount
    totalamount = amount + shipping_amount
  return render(request, 'app/checkout.html', {'add' : add, 'totalamount' : totalamount, 'cart_items' : cart_item})

@login_required
def payment_done(request):
  user = request.user
  custid = request.GET.get('custid') 
  customer = Customer.objects.get(id=custid)
  cart = Cart.objects.filter(user=user)
  for c in cart:
    OrderedPlaced(user=user, customer = customer, product = c.product, quantity = c.quantity).save()
    c.delete()
  return redirect("orders")