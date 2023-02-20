from django import forms
from .models import Product, Unit, Channel, Category, \
                    Brand, AmbienceImage, SpecificationImage, \
                    TechnicalImage, Material
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ProductForm(forms.ModelForm):
        # ------------- crispy_forms
    helper = FormHelper()
    helper.form_method = 'post'
    helper.form_class = 'form-horizontal'
    helper.label_class = 'col-md-2'
    helper.field_class = 'col-md-10'
    helper.add_input(Submit('submit', 'Save'))
    # General Information ---------------------------
    name = forms.CharField(label='Name', max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Name','style': 'width: 30%;'}))
    pim_code = forms.CharField(label='PIM Code', required=False, widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly', }))
    status = forms.ChoiceField(choices=Product.Status.choices, widget=forms.Select(attrs={'class': 'select2'}))
    prefix_code = forms.ChoiceField(label='Prefix Code', choices=Product.Prefix_code.choices, widget=forms.Select(attrs={'class': 'select2','style': 'width: 10%;'}))
    sku = forms.CharField(label='SKU', max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 20%;'}))
    featured_image = forms.ImageField(label='Featured Image',widget=forms.ClearableFileInput(attrs={'class': 'form-control','multiple': True,'style': 'width: 30%;'}), required=False)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), widget=forms.Select(attrs={'class': 'select2','style': 'width: 10%;'}), required=False)
    status = forms.ChoiceField(label='Status', choices=Product.Status.choices, widget=forms.Select(attrs={'class': 'select2','style': 'width: 10%;'}))
    unit = forms.ModelChoiceField(queryset=Unit.objects.all(), widget=forms.Select(attrs={'class': 'select2','style': 'width: 10%;'}), required=False)
    channel = forms.ModelMultipleChoiceField(queryset=Channel.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select2','style': 'width: 30%;'}), required=False)
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select2','style': 'width: 30%;'}), required=False)
    material = forms.ModelMultipleChoiceField(queryset=Material.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select2','style': 'width: 30%;'}), required=False)
    cbm = forms.DecimalField(label='cbm', max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 50%;'}))
    moq = forms.IntegerField(label='moq', initial=0, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 10%;'}))
    cost_price = forms.DecimalField(label='Cost Price', max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 20%;'}))
    # Product Specifications -----------
    ps_overal_dimension = forms.CharField(label='Overal Dimension', max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter overall dimension','style': 'width: 30%;'}))
    ps_arm_height = forms.DecimalField(label='Arm Height', max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter arm height','style': 'width: 10%;'}))
    ps_seat_height = forms.DecimalField(label='Seat Height', max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter seat height','style': 'width: 10%;'}))
    ps_seat_depth = forms.DecimalField(label='Seat Depth', max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter seat depth','style': 'width: 10%;'}))
    ps_nett_weight = forms.DecimalField(label='Nett Weight', max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter nett weight','style': 'width: 10%;'}))
    ps_gross_weight = forms.DecimalField(label='Gross Weight', max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter gross weight','style': 'width: 10%;'}))
    ps_product_type = forms.CharField(label='Product Type', max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product type','style': 'width: 20%;'}))
    ps_seat_construction = forms.CharField(label='Seat Construction', max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter seat construction','style': 'width: 20%;'}))
    # Shipping Details
    ps_box_dimension = forms.CharField(label='Box Dimension',max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Box dimension','style': 'width: 20%;'}))
    ps_box_weight = forms.CharField(label='Box Weight',max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 10%;'}))
    ps_pax = forms.CharField(label='ps pax',max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 10%;'}))
    ps_20ft_container = forms.CharField(label='20ft container',max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 10%;'}))
    ps_40gp_container = forms.CharField(label='40gp container',max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 10%;'}))
    ps_40hq_container = forms.CharField(label='40hq container',max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 10%;'}))
    # Factory Drawing ---------------
    production_drawing_pdf = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control','multiple': True,'style': 'width: 30%;'}), required=False)
    production_drawing_archive = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control','multiple': True,'style': 'width: 30%;'}), required=False)
    assembly_pdf = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control','multiple': True,'style': 'width: 30%;'}), required=False)
    assembly_archive = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control','multiple': True,'style': 'width: 30%;'}), required=False)
    bom_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control','multiple': True,'style': 'width: 30%;'}), required=False)
    # Dezign Studio
    drawing_3d_dwg = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control','multiple': True,'style': 'width: 30%;'}), required=False)
    drawing_3d_obj = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control','multiple': True,'style': 'width: 30%;'}), required=False)
    drawing_3d_3dmax = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control','multiple': True,'style': 'width: 30%;'}), required=False)
    drawing_3d_sketchup = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control','multiple': True,'style': 'width: 30%;'}), required=False)
    # SEO ----------------------
    seo_meta_title = forms.CharField(label='SEO Meta title',max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 30%;'}))
    seo_meta_description = forms.CharField(label='SEO Meta description',max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 30%;'}))
    seo_meta_keyword = forms.CharField(label='SEO Meta Keywords',max_length=200, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 30%;'}))
    seo_content_overview = forms.CharField(label='Content Overview',max_length=200, required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': '','style': 'width: 30%;'}))
    # id = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'form-control','readonly':'readonly'}))
    


    class Meta:
        model = Product
        exclude = []
        fields = [
            # General Information ---------------------
            # 'pim_code',
            'id','prefix_code','sku',  'name', 'brand', 'status',
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
            # 'featured_image': forms.ClearableFileInput(attrs={'multiple': True}),
            # 'id': forms.TextInput(attrs={'readonly': 'readonly'}),
            # 'id': forms.HiddenInput(),
        }
    #  ----------- CLEAN ----------------
    def clean_sku(self):
        sku = self.cleaned_data['sku']
        instance = getattr(self, 'instance', None)
        if instance and instance.sku == sku:
            return sku
        if Product.objects.filter(sku=sku).exists():
            raise ValidationError("A product with this SKU already exists.")
        return sku
    
    def clean_moq(self):
        moq = self.cleaned_data['moq']
        return moq if moq is not None else 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance:
            self.initial['pim_code'] = instance.pim_code
        

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['moq'].initial = 1
        

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

