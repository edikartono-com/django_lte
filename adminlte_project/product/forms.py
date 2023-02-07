from django import forms
from .models import Product, Category, Brand, AmbienceImage

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['sku', 'name', 'featured_image', 'category', 'brand', 'bom_file', 'cost_price', 'status']
        widgets = {
            # 'category': forms.CheckboxSelectMultiple,
            'featured_image': forms.ClearableFileInput(attrs={'multiple': True}),
        }

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