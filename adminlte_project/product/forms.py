from django import forms
from .models import Product, Category, Brand, AmbienceImage
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'featured_image', 'category', 'brand', 'bom_file', 'cost_price', 'status']
        widgets = {
            # 'category': forms.CheckboxSelectMultiple,
            'featured_image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        if Product.objects.filter(sku=sku).exists():
            raise ValidationError("A product with this SKU already exists.")
        return sku

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'picture']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']

class AmbienceImageForm(forms.ModelForm):
    class Meta:
        model = AmbienceImage
        fields = ['product', 'image']