from django.urls import path
from . import views

urlpatterns = [
    path('', views.adhome, name='adhome'),
    path('addandshow/',views.add_show,name='add_show'),
    path('delete_slider/<int:id>/', views.delete_slider, name='delete_slider'),
    path('navslider/edit/<int:id>/', views.edit_navslider, name='edit_navslider'),
    # for main category
    path('addandshowmain/',views.add_show_main,name='add_show_main'),
    path('delete_main/<int:id>/', views.delete_main, name='delete_main'),
    path('main/edit/<int:id>/', views.edit_main, name='edit_main'),
    # for category
    path('addandshowcate/',views.add_show_cate,name='add_show_cate'),
    path('delete_cate/<int:id>/', views.delete_cate, name='delete_cate'),
    path('cate/edit/<int:id>/', views.edit_cate, name='edit_cate'),

    # for subcategory
    path('addandshowsubcate/', views.add_show_subcate, name='add_show_subcate'),
    path('delete_subcate/<int:id>/', views.delete_subcate, name='delete_subcate'),
    path('subcate/edit/<int:id>/', views.edit_subcate, name='edit_subcate'),

    #for products
    path('addandshowproduct/', views.add_show_product, name='add_show_product'),
    path('delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('product/edit/<int:id>/', views.edit_product, name='edit_product'),

    path('users/', views.user_list, name='user_list'),
    path('delete_user/<int:id>/', views.delete_user, name='delete_user'),
    path('users/block/<int:id>/', views.block_user, name='block_user'),
    path('users/unblock/<int:id>/', views.unblock_user, name='unblock_user'),
    path('user/edit/<int:id>/', views.edit_user, name='edit_user'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminlogout/', views.logout_view, name='adminlogout'),
    path('admin/orders/', views.admin_order_list, name='admin_order_list'),



    path('add-coupon/', views.add_coupon, name='add_coupon'),
    path('delete-coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),
    path('coupons/', views.coupon_list, name='coupon_list'),


    path('admin/sales-report/', views.sales_report_view, name='sales_report'),


    path('sales-report/', views.sales_report_view, name='sales_report'),
    path('sales-report/pdf/', views.sales_report_pdf_view, name='sales_report_pdf'),


    
   
]
