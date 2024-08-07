from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
import json
import datetime
from django.contrib import messages

from .models import *
from . utils import cookieCart,cartData,guestOrder
from django_daraja.mpesa.core import MpesaClient
# Create your views here.
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    category = Category.objects.all()

    for cat in category:
        cat_products = Product.objects.filter(category=cat)
        
    context= {'products':products,'cartItems': cartItems,'cat_products':cat_products, 'categories':category}
    return render(request,'store/store.html',context)
   

def category(request, name):
    data = cartData(request)
    cartItems = data['cartItems']
    # Grab the category from the url
    try:
        category = Category.objects.get(name=name)
        cat_products = Product.objects.filter(category=category)
        return  render(request, "store/category.html", {'cat_products':cat_products, 'category':category,'cartItems':cartItems})

    except:
        messages.warning(request, "That category doesn't exist")
        return render(request,"store/category.html")

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context= {'items':items, 'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)

def checkout(request): 
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context= {'items':items, 'order':order,'cartItems':cartItems,'shipping':False}
    return render(request,'store/checkout.html',context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('productId:',productId)
    print('Action:',action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer,complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    if order.shipping ==True:
        ShippingAddress.objects.create(
            order = order,
            customer = customer,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode'],
        )

    return JsonResponse("Payment complete",safe=False)

def search(request):
    data = cartData(request)
    cartItems = data['cartItems']
    if request.method == 'GET':
        query = request.GET.get('query')

        if query:
            prod = Product.objects.filter(name__icontains=query)
            return render(request, "store/search.html", {'prod':prod,'cartItems':cartItems})

