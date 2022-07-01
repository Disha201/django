
import email
from itertools import product
from locale import currency
import math
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render

from myapp.models import Cart, Order, OrderDetails, User
from seller.models import Product

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    products=Product.objects.all()
    return render(request,'index.html',{'product':products})


def login(request):
    if request.method=="POST":
        try:
            obj = User.objects.get(email=request.POST['email'])
            if request.POST['password'] == obj.password:
                request.session['email']=request.POST['email']
                request.session['name']=obj.name
                return render(request,'index.html')

            else:
                return render(request,'login.html',{'msg':'Wrong password'}) 
        except:
                print(obj)
                return render(request,'login.html',{'msg':'Email not Register'})
        
    return render(request,'login.html')

def forgotpassword(request):
    return render(request,'forgotpassword.html')

def logout(request):
    del request.session['email']
    del request.session['name']
    return redirect('login')

def register(request):
    if request.method=="POST":
        try:
            obj=User.objects.get(email=request.POST['email'])
            return render(request,'register.html',{'msg':'Enter Unique Email'})
        except:
            if request.POST['password']==request.POST['cnpassword']:
                User.objects.create(
                    name=request.POST['name'],
                    email=request.POST['email'],
                    password=request.POST['password'],
                )
                return render(request,'login.html')
            else:
                return render(request,'register.html',{'msg':'wrong password'})
            
    return render(request,'register.html')

def products(request):
    products=Product.objects.all()
    return render(request,'products.html',{'products':products})

def single(request,pid):
    productobj=Product.objects.get(id=pid)
    return render(request,'single.html',{'productobj':productobj})

def add_to_cart(request,pid):
    pid=request.GET['id']
    pobj=Product.objects.get(id=pid)
    userobj=User.objects.get(email=request.session['email'])
    Cart.objects.create(
        product=pobj,
        quantity=1,
        user=userobj
    )
    return JsonResponse({'msg':'added to cart'})

def cart(request):
    user=User.objects.get(email=request.session['email'])
    product=Cart.objects.filter(user=user)
    n=Cart.objects.all().count()
    total=0
    for i in product:
        i.product.discountedprice=i.product.discountedprice*i.quantity
        total+=i.product.discountedprice*i.quantity
    total=float(f'{total:.1f}')

    # total+=150
    return render(request,'cart.html',{'prod':product,'count':n,'total':total})

def UpdateCartQty(request):
    cartid=request.GET['id']
    qty=request.GET['qty']
    cartobj=Cart.objects.get(id=cartid)
    cartobj.quantity=qty
    print(cartobj.quantity)
    cartobj.save()
    return JsonResponse({'msg':'Quantity Updated'})

def remove(request):
    user=User.objects.get(email=request.session['email'])
    pid=request.GET['id']
    print(pid)
    product1=Product.objects.get(id=pid)
    print(product1,user)
    
    car1=Cart.objects.get(product=product1,user=user)
    car1.delete()
    return JsonResponse({'msg':'Remove From Cart'})


def search(request):
    products=Product.objects.all()
    l=0
    search=request.GET['search']
    for i in products:
        search=search.lower()
        i.name=i.name.lower()
        if search.lower() == i.name.lower():
            l=1
        elif i.name.startswith(search):
            l=1
    print(l)
    return render(request,'search.html',{'products':products,'search':search,'l':l})




def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')


    #######    Payment    ########

razorpay_client = razorpay.Client(
	auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def checkout(request):
    userobj=User.objects.get(email=request.session['email'])
    orderobj=Order.objects.create(
        user=userobj,
        order_status='Confirmed'
    )

    carobj=Cart.objects.filter(user=userobj)
    for i in carobj:
        OrderDetails.objects.create(
            product= i.product,
            quantity=i.quantity,
            order=orderobj
        )
    total=0
    for i in carobj:
        i.product.discountedprice=i.product.discountedprice*i.quantity
        total+=i.product.discountedprice*i.quantity
    total=float(f'{total:.1f}')
    currency = 'INR'
	
    amount = total*100 # Rs. 200

	# Create a Razorpay Order
	
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
													currency=currency,
													payment_capture='0'))

	# order id of newly created order.
	
    razorpay_order_id = razorpay_order['id']
    callback_url = 'paymenthandler/'

	# we need to pass these details to frontend.
	
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    return render(request,'success.html',context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
def paymenthandler(request):

	# only accept POST request.
	if request.method == "POST":
		try:
		
			# get the required parameters from post request.
			payment_id = request.POST.get('razorpay_payment_id', '')
			razorpay_order_id = request.POST.get('razorpay_order_id', '')
			signature = request.POST.get('razorpay_signature', '')
			params_dict = {
				'razorpay_order_id': razorpay_order_id,
				'razorpay_payment_id': payment_id,
				'razorpay_signature': signature
			}

			# verify the payment signature.
			result = razorpay_client.utility.verify_payment_signature(
				params_dict)
			if result is None:
				amount = 20000 # Rs. 200
				try:
					# capture the payemt
					razorpay_client.payment.capture(payment_id, amount)

					# render success page on successful caputre of payment
					return render(request, 'paymentsuccess.html')
				except:

					# if there is an error while capturing payment.
					return render(request, 'paymentfail.html')
			else:

				# if signature verification fails.
				return render(request, 'paymentfail.html')
		except:

			# if we don't find the required parameters in POST data
			return HttpResponseBadRequest()
	else:
	# if other than POST request is made.
		return HttpResponseBadRequest()


