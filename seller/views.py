from django.http import JsonResponse
from django.shortcuts import redirect, render

from seller.models import Product, Seller

# Create your views here.
def seller_index(request):
    return render(request,'seller-index.html')

def seller_login(request):
    if request.method=='POST':
        try:
            sellerobj=Seller.objects.get(email=request.POST['email'])
            if request.POST['password']==sellerobj.password:
                print(sellerobj.email)
                request.session['email']=sellerobj.email
                request.session['name']=sellerobj.name
                return redirect('seller-index')
            else:
                return render(request,'seller-login.html',{'msg':'wrong password'})

        except:
                return render(request,'seller-login.html',{'msg':'Email not found'})


    return render(request,'seller-login.html')

def seller_logout(request):
         del request.session['email']
         del request.session['name']
         return redirect('seller-login')

def add_product(request):
    sellerobj=Seller.objects.get(email=request.session['email'])
    if request.method=='POST':
        if 'pic' in request.FILES :
            Product.objects.create (
            seller=sellerobj,
            name=request.POST['name'],
            des=request.POST['des'],
            price=request.POST['price'],
            quantity=request.POST['quantity'],
            discount=request.POST['discount'],
            discountedprice=float(request.POST['price'])-(float(request.POST['price'])*float(request.POST['discount'])/100),
            pic=request.FILES['pic'],
            pic1=request.FILES['pic1'],
            pic2=request.FILES['pic2'],
            )
            return JsonResponse({'msg': 'Product Added'})
    return render(request,'add-product.html')

def manage_products(request):
    sellerobj=Seller.objects.get(email=request.session['email'])
    plist=Product.objects.filter(seller=sellerobj)
    return render(request,'manage-products.html',{'productdata':plist})

def edit_product(request,pid):
    productobj=Product.objects.get(id = pid)
    if request.method=='POST':
        productobj.name=request.POST['name']
        productobj.des=request.POST['des']
        productobj.price=request.POST['price']
        productobj.quantity=request.POST['quantity']
        productobj.discount=request.POST['discount']
        if 'pic' in request.FILES:
            productobj.pic=request.FILES['pic']
        if 'pic1' in request.FILES:
            productobj.pic1=request.FILES['pic1']
        if 'pic2' in request.FILES:
            productobj.pic2=request.FILES['pic2']
        print(productobj.pic1)
        productobj.save()
        return JsonResponse({'msg': 'Product Edited'})
    return render(request,'edit-product.html',{'productobj':productobj})
    

def delete_product(request,pid):
    productobj=Product.objects.get(id=pid)
    productobj.delete()
    return redirect('manage-products')