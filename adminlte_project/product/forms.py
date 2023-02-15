from django import forms
from .models import Product, Unit, Channel, Category, \
                    Brand, AmbienceImage, SpecificationImage, \
                    TechnicalImage, Material
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    pim_code = forms.CharField(label='PIM Code', required=False, widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # status = forms.ChoiceField(choices=Product.Status.choices, widget=forms.Select(attrs={'class': 'select2'}))
    class Meta:
        model = Product
        exclude = []
        fields = [
            # General Information ---------------------
            'id','prefix_code','sku', 'pim_code', 'sku', 'name', 'brand', 'status',
            'featured_image', 'material', 'unit', 'channel', 'category', 'cost_price',
            'category', 'brand', 'bom_file', 'cost_price', 'status',
            # Product Specification ---------------------
            'ps_overal_dimension','ps_arm_height','ps_seat_height','ps_seat_depth',
            'ps_nett_weight', 'ps_gross_weight', 'ps_product_type','ps_seat_construction',
            # Shipping details ---------------------------------
            'ps_box_dimension','ps_box_weight', 'ps_pax', 'ps_20ft_container',
            'ps_40gp_container','ps_40hq_container', 'cbm', 'moq',
            # Factory Drawing -----------------------------------------
            'production_drawing_pdf', 'production_drawing_archive','assembly_pdf',
            'assembly_archive', 'bom_file',
            # Dezign Studio -------------------------------------------
            'drawing_3d_dwg','drawing_3d_obj','drawing_3d_3dmax','drawing_3d_sketchup',
            # SEO
            'seo_meta_title','seo_meta_description','seo_meta_keyword','seo_content_overview',
            
            ]
    
        
        widgets = {
            # 'category': forms.CheckboxSelectMultiple,
            'featured_image': forms.ClearableFileInput(attrs={'multiple': True}),
            # 'id': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'id': forms.HiddenInput(),
        }

    def clean_sku(self):
        sku = self.cleaned_data['sku']
        instance = getattr(self, 'instance', None)
        if instance and instance.sku == sku:
            return sku
        if Product.objects.filter(sku=sku).exists():
            raise ValidationError("A product with this SKU already exists.")
        return sku

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['pim_code'] = instance.pim_code
        

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'picture']

class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = ['name', 'description','picture']

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name']

class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name']

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']

class AmbienceImageForm(forms.ModelForm):
    class Meta:
        model = AmbienceImage
        fields = ['product', 'image']

class SpecificationImageForm(forms.ModelForm):
    class Meta:
        model = SpecificationImage
        fields = ['product', 'image']

class TechnicalImageForm(forms.ModelForm):
    class Meta:
        model = TechnicalImage
        fields = ['product', 'image']

