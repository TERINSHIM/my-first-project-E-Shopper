from decimal import Decimal
import json
from django.contrib import messages
from django.shortcuts import render
import razorpay
from adminside.models import *
from django.contrib.auth.decorators import login_required
from adminside.forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from datetime import timedelta
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa


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
    
    next_page = request.GET.get('next') or request.POST.get('next', 'useraddress')

    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect(next_page)  
    else:
        form = AddressForm()

    return render(request, 'userprofile/addaddress.html', {'form': form, 'next': next_page})





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

    if request.method == 'POST':
        selected_color_id = request.POST.get('color')
        selected_size_id = request.POST.get('size')

    
        

       
        cart_item, created = Cart.objects.get_or_create(
            user=request.user, 
            product=product_instance,
           
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')

    return redirect('product_detail', product_id=product_id)


@login_required(login_url='user_login')
def checkout(request):
    user = request.user
    user_addresses = Address.objects.filter(user=user)

    cart_items = Cart.objects.filter(user=user)
    subtotal = sum(item.product.price * item.quantity for item in cart_items)
    shipping = 10
    total = subtotal + shipping

    discount = request.session.get('discount', 0)
    discounted_total = request.session.get('discounted_total', subtotal)
    coupon_code = request.session.get('coupon_code')

    
    wallet, created = Wallet.objects.get_or_create(user=user)

    context = {
        'user': user,
        'addresses': user_addresses,
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': discounted_total + shipping,  
        'discount': discount,
        'coupon_code': coupon_code,
        'wallet_balance': wallet.balance  
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


@login_required(login_url='user_login')
def filter_products(request):
    price_range = request.GET.get('price_range')
    color = request.GET.get('color')
    size = request.GET.get('size')

    
    products = product.objects.all()
    if price_range:
        min_price, max_price = map(int, price_range.split('-'))
        products = products.filter(price__gte=min_price, price__lte=max_price)
    if color:
        products = products.filter(color=color)
    if size:
        products = products.filter(size=size)

    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return render(request, 'partials/_product_list.html', {'products': products})
    
    
    return render(request, 'shop.html', {'products': products})

RAZORPAY_API_KEY = "rzp_test_0e2nGCOSo0F29l"
RAZORPAY_API_SECRET = "rXAYkUaY3YntkoffZJIf6Dh5"

@login_required(login_url='user_login')
def place_order(request):
    if request.method == "POST":
        user = request.user
        payment_method = request.POST.get('payment')

        discounted_total = request.session.get('discounted_total')
        discount = request.session.get('discount', 0)

        cart_items = Cart.objects.filter(user=user)

        if not discounted_total:
            discounted_total = sum(item.product.price * item.quantity for item in cart_items)

        wallet = Wallet.objects.get(user=user)

      
        discounted_total = Decimal(discounted_total)

       
        if payment_method == 'wallet':
            if wallet.balance >= discounted_total:
               
                wallet.balance -= discounted_total
                wallet.save()

             
                order = Order.objects.create(
                    user=user,
                    payment_method='wallet',
                    total_amount=discounted_total,
                    discount=discount
                )

              
                for item in cart_items:
                    OrderItem.objects.create(
                        order=order,
                        product=item.product,
                        quantity=item.quantity,
                        price=item.product.price
                    )

              
                cart_items.delete()

             
                WalletTransaction.objects.create(
                    wallet=wallet,
                    amount=-discounted_total,
                    transaction_type='DEBIT'
                )

                messages.success(request, 'Your order has been placed successfully using your wallet balance!')
                return redirect('home')
            else:
                messages.error(request, 'Insufficient wallet balance. Please select another payment method.')

        elif payment_method == 'razorpay':
            client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET))

            order_data = {
                'amount': int(discounted_total * 100),  
                'currency': 'INR',
                'payment_capture': '1'  
            }
            razorpay_order = client.order.create(data=order_data)

            payment = Payment.objects.create(
                user=user,
                amount=discounted_total,
                razorpay_order_id=razorpay_order['id'],
                paid=False
            )

            context = {
                'user': user,
                'total_amount': int(discounted_total * 100),  
                'razorpay_order_id': razorpay_order['id'],
                'razorpay_api_key': RAZORPAY_API_KEY,
                'payment': payment,
            }

            return render(request, 'process_razorpay.html', context)

        elif payment_method == 'cash_on_delivery':
            order = Order.objects.create(
                user=user,
                payment_method=payment_method,
                total_amount=discounted_total,
                discount=discount  
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
            messages.error(request, 'Please select a valid payment method.')

    return redirect('checkout')








@login_required(login_url='user_login')
def payment_success(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('order_id')

        try:
            payment = Payment.objects.get(id=order_id, user=request.user)
            payment.razorpay_payment_id = payment_id
            payment.paid = True
            payment.save()

            order = Order.objects.create(
                user=request.user,
                payment_method='razorpay',
                total_amount=payment.amount,
                payment=payment  
            )

            cart_items = Cart.objects.filter(user=request.user)
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart_items.delete()

            messages.success(request, "Payment was successful! Your order has been placed.")

            return render(request, 'pyment_status.html')

        except Payment.DoesNotExist:
            return HttpResponse("Order does not exist.", status=400)

    return HttpResponse("Invalid request.", status=400)


@login_required(login_url='user_login')
def cancel_order(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    
    if order.status not in ['Cancelled', 'Returned']:  
        order.status = 'Cancelled'
        order.save()

       
        wallet, created = Wallet.objects.get_or_create(user=request.user)

        
        wallet.balance += order.total_amount
        wallet.save()

        
        WalletTransaction.objects.create(
            wallet=wallet,
            amount=order.total_amount,
            transaction_type='CREDIT',
            description=f"Order #{order.id} cancelled"
        )

       
        messages.success(request, "Your order has been cancelled and the amount has been credited to your wallet.")
    
    return redirect('order')


@login_required(login_url='user_login')
def return_order(request, id):
    order = get_object_or_404(Order, id=id, user=request.user)
    
    if order.status not in ['Cancelled', 'Returned']:  
        order.status = 'Returned'
        order.save()
        
        
        wallet = Wallet.objects.get(user=request.user)
        wallet.balance += order.total_amount
        wallet.save()

        WalletTransaction.objects.create(
            wallet=wallet,
            amount=order.total_amount,
            transaction_type='CREDIT',
            description=f"Order #{order.id} returned"
        )
        
        messages.success(request, "Your order has been returned and the amount has been credited to your wallet.")
    
    return redirect('order')

@login_required(login_url='user_login')
def wallet_view(request):
    
    wallet, created = Wallet.objects.get_or_create(user=request.user)

    
    transactions = WalletTransaction.objects.filter(wallet=wallet)

    context = {
        'wallet': wallet,
        'transactions': transactions,
    }
    
    return render(request, 'wallet.html', context)



@login_required(login_url='user_login')
def wishlist_view(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})


@login_required(login_url='user_login')
def add_to_wishlist(request, product_id):
    
    product_instance = get_object_or_404(product, id=product_id)

    
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product_instance)

    return redirect('wishlist_view')

@login_required(login_url='user_login')
def remove_from_wishlist(request, product_id):
    
    product_instance = get_object_or_404(product, id=product_id)
    
    
    Wishlist.objects.filter(user=request.user, product=product_instance).delete()
    
    
    return redirect('wishlist_view')



@login_required(login_url='user_login')
def move_to_cart(request, product_id):
    
    product_instance = get_object_or_404(product, id=product_id)
    
   
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product_instance)
    if not created:
       
        cart_item.quantity += 1
    cart_item.save()

   
    Wishlist.objects.filter(user=request.user, product=product_instance).delete()

    
    return redirect('wishlist_view')



@login_required(login_url='user_login')
def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon_code')
        try:
            coupon = get_object_or_404(Coupon, code=code)
            if coupon.is_valid():
               
                user = request.user
                cart_items = Cart.objects.filter(user=user)
                subtotal = sum(Decimal(item.product.price) * item.quantity for item in cart_items)
                
             
                discount = (coupon.discount / 100) * subtotal
                discounted_total = subtotal - discount
                
                
                request.session['coupon_code'] = coupon.code
                request.session['discount'] = float(discount)
                request.session['discounted_total'] = float(discounted_total)

                messages.success(request, f"Coupon '{coupon.code}' applied successfully!")
            else:
                messages.error(request, "This coupon has expired or is inactive.")
        except Coupon.DoesNotExist:
            messages.error(request, "Invalid coupon code.")
    
    return redirect('checkout')

@login_required(login_url='user_login')
def remove_coupon(request):
    if 'coupon_code' in request.session:
        del request.session['coupon_code']
        messages.success(request, "Coupon removed successfully.")
    
    return redirect('cart')


@login_required(login_url='user_login')
def generate_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    context = {
        'order': order,
    }

    template = get_template('invoice.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response


@login_required(login_url='user_login')
def download_invoice(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    subtotal = sum(item.price * item.quantity for item in order.items.all())
    delivery_charge = 10
    total_amount = subtotal + delivery_charge

  
    items = [
        {
            'product': item.product,
            'price': item.price,
            'quantity': item.quantity,
            'subtotal': item.price * item.quantity
        }
        for item in order.items.all()
    ]

    context = {
        'order': order,
        'items': items,
        'subtotal': subtotal,
        'delivery_charge': delivery_charge,
        'total_amount': total_amount,
    }

    template = get_template('invoices/invoice.html')
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{order_id}.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We encountered an error while generating your PDF.')
    return response