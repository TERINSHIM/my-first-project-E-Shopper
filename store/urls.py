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
    path('filter-products/', views.filter_products, name='filter_products'),
    path('place-order/', views.place_order, name='place_order'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('wallet/',views.wallet_view,name='wallet'),
    path('order/<int:id>/cancel/', views.cancel_order, name='cancel_order'),
    path('order/<int:id>/return/', views.return_order, name='return_order'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('move_to_cart/<int:product_id>/', views.move_to_cart, name='move_to_cart'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('remove-coupon/', views.remove_coupon, name='remove_coupon'),

    path('order/<int:order_id>/download-invoice/', views.download_invoice, name='download_invoice'),

    path('request-return-order/<int:id>/', views.request_return_order, name='request_return_order'),

    

     
    

]






