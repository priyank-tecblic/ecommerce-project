from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import Product,Cart,OrderDetail,Order,DeliveryAdress,TrackOrder
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from math import ceil
# Create your views here.

def home(request):
    if not request.user.is_authenticated:
        count = 0
    else:
        count = Cart.objects.filter(user=request.user).count()
    products = Product.objects.all()
    allproducts = []
    catproduct = Product.objects.values('pcategory','pid')
    cats  = {item['pcategory'] for item in catproduct}
    for cat in cats:
        prod = Product.objects.filter(pcategory = cat)
        n = len(prod)
        nslides = n//4 + ceil(n/4-n//4)
        allproducts.append([prod,range(1,nslides),nslides])
    # params = {'no_of_slides':nslides,'range':range(1,nslides),'product':products,"hello":"hello"}
    return render(request,'home.html',{"allproduct":allproducts,"count":count})

def signOut(request):
    logout(request)
    messages.success(request, 'you loggged out')
    return redirect('/')
    
def signUp(request):
    return render(request,'signupPage.html')

def signIn(request):
    return render(request,"signinPage.html")

def about(request):
    if not request.user.is_authenticated:
        count = 0
    else:
        count = Cart.objects.filter(user=request.user).count()
    return render(request,'about.html',{'count':count})


def saveUser(request):
    if request.method == 'POST':
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        username = request.POST.get("uname")
        password = request.POST.get("password")
        email = request.POST.get("email")
        user = User.objects.create_user(username=username,email=email,password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        messages.success(request, 'your account create successfully! click on Login')
        return redirect("/")


def checkUser(request):
    if request.method == 'POST':
        username = request.POST.get("uname")
        password = request.POST.get("password")
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, 'You logined successfully!')

            return redirect("/")
        else:
            messages.warning(request, 'invalid credentials!')
            return redirect("/signin/")

def addCart(request):
    product = Product.objects.get(pid=request.GET.get('id'))
    cartitem = Cart.objects.filter(product=product,user=request.user)
    if cartitem.count()>0:
        cartitem.update(quantity = cartitem[0].quantity+1,total = cartitem[0].total + product.price)
    else:
        cart = Cart(product = product,user=request.user,quantity=1,price=product.price,total=product.price)
        cart.save()
    return redirect("/")


def cartView(request):
    if not request.user.is_authenticated:
        count = 0
    else:
        count = Cart.objects.filter(user=request.user).count()
    cart = Cart.objects.filter(user = request.user)
    alltotal = 0
    for i in cart:
        alltotal = alltotal + i.total
    return render(request,'cart.html',{'count':count,'cart':cart,'alltotal':alltotal})

def plus(request):
    cart = Cart.objects.filter(cid=request.GET.get('id'))
    cart.update(quantity=cart[0].quantity+1,total=cart[0].total+cart[0].price)
    return redirect('/cart')

def minus(request):
    cart = Cart.objects.filter(cid=request.GET.get('id'))
    cart.update(quantity=cart[0].quantity-1,total=cart[0].total-cart[0].price)
    if cart[0].quantity == 0:
        cart.delete()
    return redirect('/cart')

def emptyCart(request):
    cart = Cart.objects.all().delete()
    return redirect("/cart")

def placeOrder(request):

    return render(request,"email.html")

def deliveryAdress(request):
    if not request.user.is_authenticated:
        count = 0
    else:
        count = Cart.objects.filter(user=request.user).count()
    cart = Cart.objects.filter(user = request.user)
    return render(request,'deliveryadress.html',{'count':count})

def placeOrder(request):
    if request.method == "POST":
        order = Order(user=request.user)
        order.save()
        deliveryadress = DeliveryAdress(order=order,user=request.user,name=request.POST.get("name","dafualt"),email=request.POST.get("email","dafualt"),add1=request.POST.get("add1","dafualt"),add2=request.POST.get("add2","dafualt"),city=request.POST.get("city","dafualt"),state=request.POST.get("state","dafualt"),zip=request.POST.get("zip","dafualt"),phone=request.POST.get("phone","dafualt"))
        deliveryadress.save()
        cart = Cart.objects.filter(user = request.user)
        for i in cart:
            orderdetail = OrderDetail(order=order,product=i.product,quantity=i.quantity,price=i.price,total=i.total)
            orderdetail.save()
        cart.delete()
        messages.success(request, f'Your order successfully placed! your order id is {order.oid}')
        return redirect("/")

def trackOrder(request):
    if not request.user.is_authenticated:
        count = 0
    else:
        count = Cart.objects.filter(user=request.user).count()
    return render(request,'trackorder.html',{'count':count})

def trackingOrder(request):
    if not request.user.is_authenticated:
        count = 0
    else:
        count = Cart.objects.filter(user=request.user).count()
    if request.method == "GET":
        order = Order(oid = request.GET.get("orderid"))
        trackorder = TrackOrder.objects.filter(order = order)
        print(trackorder)
    return render(request,'trackorder.html',{'count':count,'trackorder':trackorder})

def search(request):
    res = request.GET.get("search")
    allproducts = []
    catproduct = Product.objects.values('pcategory','pid')
    product = Product.objects.filter(pname__icontains=res) | Product.objects.filter (pcategory__icontains=res) | Product.objects.filter(psubcategory__icontains=res)| Product.objects.filter(pdesc__icontains=res)
    cats  = {item['pcategory'] for item in catproduct}
    for cat in cats:
        prod = product.filter(pcategory = cat)
        if prod:
            n = len(prod)
            nslides = n//4 + ceil(n/4-n//4)
            allproducts.append([prod,range(1,nslides),nslides])
    return render(request,'search.html',{"search":res,"allproduct":allproducts})

def myOrder(request):
    if not request.user.is_authenticated:
        count = 0
    else:
        count = Cart.objects.filter(user=request.user).count()
    orderdetaillist=[]
    order = Order.objects.filter(user=request.user)[::-1]
    for i in order:
        orderdetail = OrderDetail.objects.filter(order=i)
        orderdetaillist.append(orderdetail)
    print(orderdetaillist)
    totalList = []
    total=0
    for k,i in zip(range(len(orderdetaillist)),orderdetaillist):
        total=0
        for j in i:
            total = total + j.total
        totalList.append(total)
    print(totalList)
    listt = zip(orderdetaillist,totalList)
    return render(request,"myorder.html",{'list':listt,'count':count,'totalList':totalList})