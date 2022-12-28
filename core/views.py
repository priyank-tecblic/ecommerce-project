from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from .models import Product,Cart,OrderDetail,Order,DeliveryAdress,TrackOrder,Coupen,Review,ProductComment
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from math import ceil
from core.templatetags import extras
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

def productView(request):
    if not request.user.is_authenticated:
        count = 0
    else:
        count = Cart.objects.filter(user=request.user).count()
    
    product = Product.objects.get(pid = request.GET.get("id"))
    try:
        rev = Review.objects.get(user=request.user,product=product)
    except Review.DoesNotExist:
        rev = None
    productcomment = ProductComment.objects.filter(product = product,parent = None)
    productreply = ProductComment.objects.filter(product = product).exclude(parent=None)
    replydict = {}
    for reply in productreply:
        if reply.parent.cno not in replydict:
            replydict[reply.parent.cno] = [reply]
        else:
            replydict[reply.parent.cno].append(reply)
    return render(request,'product.html',{'count':count,'product':product,'review':rev,'comments':productcomment,"replydict":replydict})

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
    promo = Coupen.objects.filter(user = request.user,applied = True)
    for i in cart:
        alltotal = alltotal + i.total
    for i in promo:
        alltotal = alltotal - i.discount
        return render(request,'cart.html',{'count':count,'cart':cart,'alltotal':alltotal,'promocode':promo[0]})
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
        promo = Coupen.objects.filter(user = request.user,applied = True).delete()
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
    if not request.user.is_authenticated:
        count = 0
    else:
        count = Cart.objects.filter(user=request.user).count()
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
    return render(request,'search.html',{"search":res,"allproduct":allproducts,'count':count})

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

def addPromoCode(request):
    promocode = request.POST.get("code")
    promoDiscount = Coupen.objects.filter(code = promocode)
    if promoDiscount is not None:
        promoDiscount.update(applied = True,user = request.user)
    return redirect("/cart")

def removePromo(request):
    promoDiscount = Coupen.objects.filter(user = request.user,applied = True)
    if promoDiscount is not None:
        promoDiscount.update(applied = False,user = None)
    return redirect("/cart")

def review(request):
    pid = request.GET.get("id")
    star = request.GET.get("rating")
    product=Product.objects.get(pid=pid)
    try:
        rev = Review.objects.get(user=request.user,product=product)
    except Review.DoesNotExist:
        rev = None
    if rev is not None:
        Review.objects.filter(user=request.user,product=product).update(star = star)
    else:
        rev = Review(star=star,user=request.user,product=product)
        rev.save()
    return redirect(f"/productview?id={pid}")

def postcomment(request):
    if request.method == 'POST':
        comment = request.POST.get("comment")
        pid = request.POST.get("pid")
        product=Product.objects.get(pid=pid)
        productcomment = ProductComment(user = request.user,product = product,comment = comment)
        productcomment.save()
        messages.success(request,"Your Comment has been posted successfully")
        return redirect(f"/productview?id={pid}")

def postreply(request):
    if request.method == 'POST':
        reply = request.POST.get("reply")
        pid = request.POST.get("pid")
        product=Product.objects.get(pid=pid)
        comment = ProductComment.objects.get(cno = request.POST.get("cno"))
        productcomment = ProductComment(user = request.user,product = product,comment = reply,parent = comment)
        productcomment.save()
        messages.success(request,"Your Reply has been posted successfully")
        return redirect(f"/productview?id={pid}")