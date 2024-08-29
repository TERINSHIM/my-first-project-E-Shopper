from django import forms
from .models import *

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
        fields = '__all__'

class AdditionalImageForm(forms.ModelForm):
    class Meta:
        model = AdditionalImage
        fields = ['image']

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
    COLOR_CHOICES = [
        ('Black', 'Black'),
        ('White', 'White'),
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
    ]
    SIZE_CHOICES = [
        ('XS', 'XS'),
        ('S', 'S'),
        ('M', 'M'),
        ('L', 'L'),
        ('XL', 'XL'),
    ]

    price_range = forms.ChoiceField(choices=PRICE_CHOICES, required=False)
    color = forms.ChoiceField(choices=COLOR_CHOICES, required=False)
    size = forms.ChoiceField(choices=SIZE_CHOICES, required=False)
