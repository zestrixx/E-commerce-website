import json
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Product, Contact, Order, OrderUpdate, BannerImage
from math import ceil
from django.views.decorators.csrf import csrf_exempt
from .Paytm import Checksum

MERCHANT_KEY = 'gX0PBOIE!Wns50uM'

def home(request):
    banner_image = BannerImage.objects.all()
    return render(request, 'shop/home.html', {'images': banner_image})


def index(request):
    allProds = []
    catprods = Product.objects.values('subcategory', 'id')
    cats = {item["subcategory"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(subcategory=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, 'shop/index.html', params)


def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    if request.method == 'POST':
        name = request.POST.get('name', "")
        phone = request.POST.get('phone', "")
        email = request.POST.get('email', "")
        query = request.POST.get('query', "")
        contact = Contact(name=name, email=email, phone=phone, query=query)
        contact.save()
        messages.success(request, 'Success')
    return render(request, 'shop/contact.html')


def tracker(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    if request.method == "POST":
        orderId = request.POST.get('orderId', "")
        phone = request.POST.get('phone', "")
        try:
            order = Order.objects.filter(order_id=orderId, phone=phone)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(
                        [updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('Not Found')
        except Exception as e:
            return HttpResponse('Error Finding Products')

    return render(request, 'shop/tracker.html')


def men(request):
    allProds = []
    catprods = Product.objects.values('subcategory')
    cats = {item["subcategory"] for item in catprods}
    for cat in cats:
        if 'Men' in cat:
            prod = Product.objects.filter(subcategory=cat)
            allProds.append(prod)
    params = {'allProds': allProds}
    return render(request, 'shop/men.html', params)


def women(request):
    allProds = []
    catprods = Product.objects.values('subcategory')
    cats = {item["subcategory"] for item in catprods}
    for cat in cats:
        if 'Women' in cat:
            prod = Product.objects.filter(subcategory=cat)
            allProds.append(prod)
    params = {'allProds': allProds}
    return render(request, 'shop/women.html', params)



def productView(request, proid):
    # fetch the product using id
    product = Product.objects.filter(id=proid)
    return render(request, 'shop/productview.html', {'product': product[0]})


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('Login')
    if request.method == 'POST':
        itemsJson = request.POST.get('itemsJson', "")
        name = request.POST.get('name', "")
        amount = request.POST.get('amount', "")
        phone = request.POST.get('phone', "")
        address = request.POST.get('address', "")
        localaddress = request.POST.get('localaddress', "")
        city = request.POST.get('city', "")
        state = request.POST.get('state', "")
        pin_code = request.POST.get('pincode', "")
        orders = Order(items_json=itemsJson, name=name, address=address, local_address=localaddress,
                       city=city, state=state, pin_code=pin_code, phone=phone, amount=amount)
        orders.save()
        update = OrderUpdate(order_id=orders.order_id,
                             update_desc="Your order has been placed")
        update.save()

        thank = True
        id = orders.order_id
        # return render(request, 'shop/checkout.html', {'thank': thank, 'id': id})
        # request paytm to transfer the amount to your account after payment by the user
        param_dict = {

            'MID': 'EMWQOt56140700859183',
            'ORDER_ID': str(orders.order_id),
            'TXN_AMOUNT': str(amount),
            'CUST_ID': phone,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/paymentstatus/',

        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict})
    return render(request, 'shop/checkout.html')


@csrf_exempt
# csrf will be bypassed when paytm send a post request to this end point
def handlerequest(request):
    # paytm will send post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            # print('Order Successful')
            pass
        else:
            pass
            # print('Order Failure because ' + response_dict['RESPMSG'])
    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search')
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": ""}
    if len(allProds) == 0 or len(query)<4:
        params = {'msg': "Please make sure to enter relevant search query"}
    return render(request, 'shop/search.html', params)
