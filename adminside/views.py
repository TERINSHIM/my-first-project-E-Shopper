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


# Create your views here.

def superuser_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_superuser, login_url='adminlogin'
    )(view_func)
    return decorated_view_func

@superuser_required
def adhome(request):
    return render(request,'adminbase.html')

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

            form = ProductForm()  # Reset form after successful submission
            formset = AdditionalImageFormSet(queryset=AdditionalImage.objects.none())  # Reset formset
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
    formset = AdditionalImageFormSet(queryset=AdditionalImage.objects.filter(product=product_instance))
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product_instance)
        formset = AdditionalImageFormSet(request.POST, request.FILES, queryset=AdditionalImage.objects.filter(product=product_instance))
        
        if form.is_valid() and formset.is_valid():
            form.save()
            
            for form in formset:
                if form.is_valid() and form.cleaned_data:
                    image = form.cleaned_data['image']
                    AdditionalImage.objects.create(product=product_instance, image=image)

            return redirect('add_show_product')
    else:
        form = ProductForm(instance=product_instance)
    
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

