from django.urls import path
from . import views




urlpatterns = [
    path('',views.home,name='home'),
    path('shop',views.shop,name='shop'),
    path('product/<str:slug>',views.product_detail,name='product_detail'),
    path('userprofile/',views.userprofile,name='userprofile'),
    path('useraddress/',views.useraddress,name='useraddress'),
    path('addaddress/', views.addaddress, name='addaddress'),
    path('editaddress/<int:id>/', views.editaddress, name='editaddress'),
    path('deleteaddress/<int:id>/', views.deleteaddress, name='deleteaddress'),
    path('cart/', views.cart_view, name='cart'),
    path('cart/remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('place_order/', views.place_order, name='place_order'),
    path('order/',views.order,name='order'),
    path('orderdetails/<int:id>/', views.order_details, name='orderdetails'),
    

     
    

]






