"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',views.home,name="Home"),
    path('signin/',views.signIn,name="SignIn"),
    path('signup/',views.signUp,name="SignUp"),
    path('about/',views.about,name="About"),
    path('saveuser/',views.saveUser,name="SaveUser"),
    path('checkuser/',views.checkUser,name="CheckUser"),
    path("addcart/", views.addCart, name="AddToCart"),
    path('signout/',views.signOut,name="SignOut"),
    path('cart/',views.cartView,name="Cart"),
    path('plus/',views.plus,name="PlusCart"),
    path('minus/',views.minus,name="MinusCart"),
    path('emptycart/',views.emptyCart,name="EmptyCart"),
    path('deliveryaddress/',views.deliveryAdress,name="DeliveryAdress"),
    path('placeorder/',views.placeOrder,name="PlaceOrder"),
    path('trackorder/',views.trackOrder,name="TrackOrder"),
    path('trackingorder/',views.trackingOrder,name="TrackingOrder")

]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
