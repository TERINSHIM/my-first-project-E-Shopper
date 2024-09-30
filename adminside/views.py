from pyexpat.errors import messages
from django.forms import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib import auth, messages
AdditionalImageFormSet = modelformset_factory(AdditionalImage, form=AdditionalImageForm, extra=3)
from .forms import ProductForm, AdditionalImageFormSet 
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.shortcuts import render
from .models import Order
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta


# Create your views here.

def superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_superuser, login_url='adminlogin'
    )(view_func)
    return decorated_view_func

@superuser_required
def adhome(request):
    print(type(request))  # Ensure this is a HttpRequest object, not a str
    print(request.user)    # Ensure this outputs a user object
    
    

    

    return render(request, 'adminbase.html')

#adminlogin
def adminlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('adhome') 
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('adminlogin')  
    return render(request, 'adminlogin.html')




@superuser_required
def add_show(request):
    if request.method == 'POST':
        fm = NavSliderForm(request.POST, request.FILES)  
        if fm.is_valid():
            fm.save()
            fm=NavSliderForm()
            
    else:
        fm = NavSliderForm()
    sliders = nav_slider.objects.all()

    return render(request, 'addandshow.html', {'form': fm,'sliders': sliders})

@superuser_required
def delete_slider(request, id):
    slider = get_object_or_404(nav_slider, id=id)
    slider.delete()
    return redirect('add_show')

@superuser_required
def edit_navslider(request, id):
    nav_slider_instance = get_object_or_404(nav_slider, id=id)
    
    if request.method == 'POST':
        form = NavSliderForm(request.POST, request.FILES, instance=nav_slider_instance)
        if form.is_valid():
            form.save()
            return redirect('add_show')  
    else:
        form = NavSliderForm(instance=nav_slider_instance)
    
    return render(request, 'edit_navslider.html', {'form': form})


#for maincategory
@superuser_required
def add_show_main(request):
    if request.method == 'POST':
        fm = MainCategoryForm(request.POST, request.FILES)  
        if fm.is_valid():
            fm.save()
            fm=MainCategoryForm()
            
    else:
        fm = MainCategoryForm()
    maincate = maincategory.objects.all()

    return render(request, 'maincategory/addandshow_maincate.html', {'form': fm,'maincate': maincate})

@superuser_required
def delete_main(request, id):
    slider = get_object_or_404(maincategory, id=id)
    slider.delete()
    return redirect('add_show_main')

@superuser_required
def edit_main(request, id):
    main_category_instance = get_object_or_404(maincategory, id=id)
    
    if request.method == 'POST':
        form = MainCategoryForm(request.POST, request.FILES, instance=main_category_instance)
        if form.is_valid():
            form.save()
            return redirect('add_show_main')  
    else:
        form = MainCategoryForm(instance=main_category_instance)
    
    return render(request, 'maincategory/edit_maincate.html', {'form': form})


# for category
@superuser_required
def add_show_cate(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('add_show_cate')  
    else:
        form = CategoryForm()

    categories = category.objects.all()
    return render(request, 'category/addandshow_cate.html', {'form': form, 'category': categories})

@superuser_required
def delete_cate(request, id):
    cate = get_object_or_404(category, id=id)
    cate.delete()
    return redirect('add_show_cate')

@superuser_required
def edit_cate(request, id):
    category_instance = get_object_or_404(category, id=id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category_instance)
        if form.is_valid():
            form.save()
            return redirect('add_show_cate')  
    else:
        form = CategoryForm(instance=category_instance)
    
    return render(request, 'category/edit_cate.html', {'form': form})


#for suncategory
@superuser_required
def add_show_subcate(request):
    if request.method == 'POST':
        fm = SubCategoryForm(request.POST)  
        if fm.is_valid():
            fm.save()
            fm = SubCategoryForm()
    else:
        fm = SubCategoryForm()
    
    subcategories =subcategory.objects.all()
    categories = category.objects.all()  

    return render(request, 'subcategory/addandshow_subcate.html', {'form': fm, 'subcategories': subcategories, 'categories': categories})
@superuser_required
def delete_subcate(request, id):
    subcate = get_object_or_404(subcategory, id=id)
    subcate.delete()
    return redirect('add_show_subcate')
@superuser_required
def edit_subcate(request, id):
    subcate_instance = get_object_or_404(subcategory, id=id)
    
    if request.method == 'POST':
        form = SubCategoryForm(request.POST, instance=subcate_instance)
        if form.is_valid():
            form.save()
            return redirect('add_show_subcate')
    else:
        form = SubCategoryForm(instance=subcate_instance)
    
    return render(request, 'subcategory/edit_subcate.html', {'form': form})





@superuser_required
def add_show_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        formset = AdditionalImageFormSet(request.POST, request.FILES, queryset=AdditionalImage.objects.none())
        
        if form.is_valid() and formset.is_valid():
            product_instance = form.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    AdditionalImage.objects.create(product=product_instance, image=image)

            form = ProductForm()  
            formset = AdditionalImageFormSet(queryset=AdditionalImage.objects.none()) 
    else:
        form = ProductForm()
        formset = AdditionalImageFormSet(queryset=AdditionalImage.objects.none())
    
    products = product.objects.all()
    categories = category.objects.all()  

    return render(request, 'product/addandshow_product.html', {'form': form, 'formset': formset, 'products': products, 'categories': categories})
@superuser_required
def delete_product(request, id):
    Product = get_object_or_404(product, id=id)
    Product.delete()
    return redirect('add_show_product')

@superuser_required
def edit_product(request, id):
    product_instance = get_object_or_404(product, id=id)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_instance)
        formset = AdditionalImageFormSet(request.POST, request.FILES, instance=product_instance)

        if form.is_valid():
            print("Product form is valid")
        else:
            print("Product form is not valid")
            print(form.errors)

        if formset.is_valid():
            print("Formset is valid")
            for form in formset:
                print(form.cleaned_data)
        else:
            print("Formset is not valid")
            print(formset.errors)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            
           
            for form in formset:
                if form.cleaned_data and form.cleaned_data.get('image'):
                    image = form.cleaned_data['image']
                    AdditionalImage.objects.create(product=product_instance, image=image)

            return redirect('add_show_product')
    else:
        form = ProductForm(instance=product_instance)
        formset = AdditionalImageFormSet(instance=product_instance)

    return render(request, 'product/edit_product.html', {'form': form, 'formset': formset})


@superuser_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})
@superuser_required
def block_user(request, id):
    user_instance = get_object_or_404(User, id=id)
    user_instance.is_active = False
    user_instance.save()
    return redirect('user_list')
@superuser_required
def unblock_user(request, id):
    user_instance = get_object_or_404(User, id=id)
    user_instance.is_active = True
    user_instance.save()
    return redirect('user_list')
@superuser_required
def delete_user(request, id):
    user_instance = get_object_or_404(User, id=id)
    user_instance.delete()
    return redirect('user_list')

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_staff']
@superuser_required
def edit_user(request, id):
    user_instance = get_object_or_404(User, id=id)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user_instance)
        if form.is_valid():
            form.save()
            return redirect('user_list') 
    else:
        form = UserEditForm(instance=user_instance)
    
    return render(request, 'users/edit_user.html', {'form': form})


@superuser_required
def admin_order_list(request):
    orders = Order.objects.all()

    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('admin_order_list')

    return render(request, 'admin_order_list.html', {'orders': orders})


def logout_view(request):
    logout(request)
    return redirect('adminlogin')



@superuser_required
def add_coupon(request):
    if request.method == 'POST':
        form = CouponForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coupon created successfully.')
            return redirect('coupon_list')  
    else:
        form = CouponForm()
    
    return render(request, 'coupon/add_coupon.html', {'form': form})

@superuser_required
def delete_coupon(request, coupon_id):
    coupon = get_object_or_404(Coupon, id=coupon_id)
    if request.method == 'POST':
        coupon.delete()
        messages.success(request, 'Coupon deleted successfully.')
        return redirect('coupon_list') 
    
    return render(request, 'coupon/delete_coupon.html', {'coupon': coupon})

@superuser_required
def coupon_list(request):
    coupons = Coupon.objects.all()
    return render(request, 'coupon/coupon_list.html', {'coupons': coupons})



@superuser_required
def sales_report_view(request):
    filter_option = request.GET.get('filter', 'custom')
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    
    today = timezone.now().date()

    if filter_option == 'daily':
        start_date = today
        end_date = today
    elif filter_option == 'weekly':
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif filter_option == 'monthly':
        start_date = today.replace(day=1)
        end_date = today
    elif filter_option == 'custom' and start_date and end_date:
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

    
    orders = Order.objects.filter(order_date__date__range=[start_date, end_date])

   
    total_sales = orders.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    total_orders = orders.count()

   
    total_discounts = 0
    for order in orders:
        total_discounts += sum(item.price * item.quantity - item.product.price * item.quantity for item in order.items.all())

    net_sales = total_sales - total_discounts

    context = {
        'orders': orders,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_discounts': total_discounts,
        'net_sales': net_sales,
        'start_date': start_date,
        'end_date': end_date,
        'filter_option': filter_option,
    }

    return render(request, 'sales_report.html', context)

@superuser_required
def sales_report_pdf_view(request):
    filter_option = request.GET.get('filter', 'custom')
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    today = timezone.now().date()

    if filter_option == 'daily':
        start_date = today
        end_date = today
    elif filter_option == 'weekly':
        start_date = today - timedelta(days=today.weekday())
        end_date = today
    elif filter_option == 'monthly':
        start_date = today.replace(day=1)
        end_date = today
    elif filter_option == 'custom' and start_date and end_date:
        start_date = timezone.datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date, '%Y-%m-%d').date()

    orders = Order.objects.filter(order_date__date__range=[start_date, end_date])
    total_sales = orders.aggregate(total_sales=Sum('total_amount'))['total_sales'] or 0
    total_orders = orders.count()

    total_discounts = 0
    for order in orders:
        total_discounts += sum(item.price * item.quantity - item.product.price * item.quantity for item in order.items.all())

    net_sales = total_sales - total_discounts

    context = {
        'orders': orders,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_discounts': total_discounts,
        'net_sales': net_sales,
        'start_date': start_date,
        'end_date': end_date,
        'filter_option': filter_option,
    }

  
    template = get_template('sales_report.html')
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    
    return response


@superuser_required
def get_top_products_and_subcategories(time_filter=None):
  
    if time_filter == 'monthly':
        filter_date = timezone.now() - timezone.timedelta(days=30)
    elif time_filter == 'yearly':
        filter_date = timezone.now() - timezone.timedelta(days=365)
    else:
        filter_date = None

   
    if filter_date:
        top_products = Sale.objects.filter(sale_date__gte=filter_date) \
            .values('product__title') \
            .annotate(total_sold=Sum('quantity')) \
            .order_by('-total_sold')[:10]
    else:
        top_products = Sale.objects.values('product__title') \
            .annotate(total_sold=Sum('quantity')) \
            .order_by('-total_sold')[:10]

   
    if filter_date:
        top_subcategories = Sale.objects.filter(sale_date__gte=filter_date) \
            .values('product__category__subcategory__title') \
            .annotate(total_sold=Sum('quantity')) \
            .order_by('-total_sold')[:10]
    else:
        top_subcategories = Sale.objects.values('product__category__subcategory__title') \
            .annotate(total_sold=Sum('quantity')) \
            .order_by('-total_sold')[:10]

    return top_products, top_subcategories


