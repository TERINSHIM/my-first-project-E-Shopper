from django import forms
from .models import *
from django.forms import inlineformset_factory

class NavSliderForm(forms.ModelForm):
    class Meta:
        model = nav_slider
        fields = '__all__'

class MainCategoryForm(forms.ModelForm):
    class Meta:
        model = maincategory
        fields = '__all__'

class CategoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = ['title', 'image', 'maincategory']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if category.objects.filter(title=title).exists():
            raise forms.ValidationError("A category with this title already exists.")
        return title

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = subcategory
        fields = '__all__'

class ProductForm(forms.ModelForm):
    class Meta:
        model = product
        fields = ['title', 'category', 'price', 'discount', 'Featured_image', 'total', 'description', 'product_information', 'tags', 'slug', 'additional_info', 'colors', 'sizes']
        widgets = {
            'colors': forms.CheckboxSelectMultiple, 
            'sizes': forms.CheckboxSelectMultiple,   
        }  

class AdditionalImageForm(forms.ModelForm):
    class Meta:
        model = AdditionalImage
        fields = ['image']

AdditionalImageFormSet = inlineformset_factory(
    product, AdditionalImage, form=AdditionalImageForm, extra=1, can_delete=True
)

class OffersForm(forms.ModelForm):
    class Meta:
        model = offers
        fields = '__all__'

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line1', 'address_line2', 'city', 'state', 'zipcode', 'country']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

class ProductFilterForm(forms.Form):
    PRICE_CHOICES = [
        ('0-100', '$0 - $100'),
        ('100-200', '$100 - $200'),
        ('200-300', '$200 - $300'),
        ('300-400', '$300 - $400'),
        ('400-500', '$400 - $500'),
    ]
    
    
    color = forms.ModelChoiceField(queryset=Color.objects.all(), required=False, empty_label="Any Color")
    size = forms.ModelChoiceField(queryset=Size.objects.all(), required=False, empty_label="Any Size")

    price_range = forms.ChoiceField(choices=PRICE_CHOICES, required=False)




class CouponForm(forms.ModelForm):
    class Meta:
        model = Coupon
        fields = ['code', 'discount', 'valid_from', 'valid_to', 'is_active']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

   
