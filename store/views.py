import json
from django.contrib import messages
from django.shortcuts import render
from adminside.models import *
from django.contrib.auth.decorators import login_required
from adminside.forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse


def home(request):
    category=maincategory.objects.all()
    slider=nav_slider.objects.all()
    Product=product.objects.all()
    offer=offers.objects.all()
    context={
        'slider':slider  ,
        'category':category ,
        'products':Product,
        'offers':offer,
    }
    return render(request,'home.html',context)

@login_required(login_url='user_login')
def shop(request):
    category=maincategory.objects.all()
    slider=nav_slider.objects.all()
    Product=product.objects.all()
    context={
        'slider':slider  ,
        'category':category ,
        'products':Product,

    }
    return render(request,'shop.html',context)

@login_required(login_url='user_login')
def product_detail(request, slug):
    Product = product.objects.get(slug=slug)
    slider = nav_slider.objects.all()
    category = maincategory.objects.all()
    

    additional_img = AdditionalImage.objects.filter(product=Product)  
    

    related_products = product.objects.filter(category=Product.category).exclude(id=Product.id)[:4] 

    context = {
        'product': Product,
        'slider': slider,
        'category': category,
        'additional_img': additional_img,
        'related_products': related_products
    }
    return render(request, 'product_detailpage.html', context)



@login_required(login_url='user_login')
def userprofile(request):
    return render(request,'userprofile/userprofilehome.html')

@login_required(login_url='user_login')
def useraddress(request):
    addresses = Address.objects.filter(user=request.user)  
    return render(request, 'userprofile/useraddress.html', {'addresses': addresses})


@login_required(login_url='user_login')
def addaddress(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('useraddress')  
    else:
        form = AddressForm()
    return render(request, 'userprofile/addaddress.html', {'form': form})



@login_required(login_url='user_login')
def editaddress(request, id):
    address = get_object_or_404(Address, id=id)
    form = AddressForm(instance=address)

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('useraddress')

    return render(request, 'userprofile/editaddress.html', {'form': form, 'address': address})


@login_required(login_url='user_login')
def deleteaddress(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    if request.method == 'POST':
        address.delete()
        return redirect('useraddress')  
    return render(request, 'userprofile/deleteaddress.html', {'address': address})

@login_required(login_url='user_login')
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    subtotal = sum(item.total_price for item in cart_items)
    shipping = 10 
    total = subtotal + shipping

    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }
    return render(request, 'cart.html', context)

@login_required(login_url='user_login')
def remove_from_cart(request, id):
    cart_item = get_object_or_404(Cart, id=id, user=request.user)
    cart_item.delete()
    return redirect('cart')

@login_required(login_url='user_login')
def add_to_cart(request, product_id):
   
    product_instance = get_object_or_404(product, id=product_id)
    
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product_instance)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart')


@login_required(login_url='user_login')
def checkout(request):
    user = request.user
    user_addresses = Address.objects.filter(user=user)

    
    cart_items = Cart.objects.filter(user=user)
    subtotal = sum(item.total_price for item in cart_items)
    shipping = 10 
    total = subtotal + shipping

    context = {
        'user': user,
        'addresses': user_addresses,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
    }

    return render(request, 'checkout.html', context)


@login_required(login_url='user_login')
def update_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        cart_item_id = data.get('id')
        quantity = data.get('quantity')

        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()  

       
        cart_items = Cart.objects.filter(user=request.user)
        subtotal = sum(item.total_price for item in cart_items)
        shipping = 10  
        total = subtotal + shipping

        return JsonResponse({
            'success': True,
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
        })

    return JsonResponse({'success': False}, status=400)


@login_required(login_url='user_login')
def place_order(request):
    if request.method == 'POST':
        payment_method = request.POST.get('payment')

        if payment_method:
          
            cart_items = Cart.objects.filter(user=request.user)
            total_amount = sum(item.product.price * item.quantity for item in cart_items)
            order = Order.objects.create(
                user=request.user,
                payment_method=payment_method,
                total_amount=total_amount
            )

         
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

           
            cart_items.delete()

      
            messages.success(request, 'Your order has been placed successfully!')

        
            return redirect('home')
        else:
            messages.error(request, 'Please select a payment method.')

    return redirect('checkout')


@login_required(login_url='user_login')
def order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'userprofile/order.html', {'orders': orders})


@login_required(login_url='user_login')
def order_details(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    subtotal = sum(item.price * item.quantity for item in order.items.all())
    delivery_charge = 10
    total_amount = subtotal + delivery_charge

    return render(request, 'userprofile/order_details.html', {
        'order': order,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'total_amount': total_amount,
    })

