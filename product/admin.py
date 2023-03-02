from django.contrib import admin
from django.contrib.admin.options import TabularInline
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import RelatedFieldListFilter
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.filters import ListFilter
from django.shortcuts import render, get_object_or_404
# import requests
from django.http import HttpResponse
from django.core.files.storage import DefaultStorage
import zipfile
import os

# from django.http import FileResponse

# from fieldsets_with_inlines import FieldsetsInlineMixin
from .models import (
    Product,
    Unit,
    Channel,
    Category,
    AmbienceImage,
    SpecificationImage,
    TechnicalImage,
    # Activity,
    # Retailer,
    Brand,
    Material,
    
)

from . import forms as frm

import admin_thumbnails
from django.template.loader import get_template
from django.utils.html import format_html
# from .resources import MyModelResource

IMAGE_TEXT = 'NOTE: custom multiple select will be provided on the frontend'

# class CategoryFilter(RelatedFieldListFilter):
#     title = 'Category'
#     parameter_name = 'category'

#     def field(self):
#         return Product._meta.get_field('category')


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id','name',]

# -------------- Activity ------------------------------
# @admin.register(Activity)
# class ActivityAdmin(admin.ModelAdmin):
#     list_display = ['user_id', 'activity_description']

# ------------- Channel & Category -------------------
@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    list_display = ['id','name','picture']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name','picture']

# ---------------- Inline ------------------

class SpecificationImageInline(TabularInline):
    @admin.display(description='Specification image display')
    def specification_image_preview(self, obj):
        return format_html('<img src="{}" style="max-width:300px; max-height:300px"/>'.format(obj.image.url))
    extra = 1
    model = SpecificationImage
    readonly_fields = ('specification_image_preview',)
    fields = ['specification_image_preview','image']
    insert_after = 'ps_seat_construction'


class AmbienceImageInline(TabularInline):
    @admin.display(description='Ambience image display')
    def ambience_image_preview(self, obj):
        return format_html('<img src="{}" style="max-width:300px; max-height:300px"/>'.format(obj.image.url))
    extra = 1
    model = AmbienceImage
    readonly_fields = ('ambience_image_preview',)
    fields = ['ambience_image_preview','image']
    insert_after = 'bom_file'


class TechnicalImageInline(TabularInline):
    @admin.display(description='Technical image display')
    def technical_image_preview(self, obj):
        return format_html('<img src="{}" style="max-width:300px; max-height:300px"/>'.format(obj.image.url))
    extra = 1
    model = TechnicalImage
    readonly_fields = ('technical_image_preview',)
    fields = ['technical_image_preview','image']
    insert_after = 'drawing_3d_sketchup'

# ------------ Product -----------------
# general information, seo marketing, dezign studio, technical drawing,
# product specification
@admin.register(Product)
@admin_thumbnails.thumbnail('featured_image','Thumbnail')
class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    
    @admin.display(description='Featured image display')
    def featured_image_preview(self, obj):
        return format_html(
            f'''<img src="{obj.featured_image.url}" style="max-width:500px; max-height:500px"/>'''
        )
    
    # @admin.display(description="Specification Image")
    # def specification_image_inline(self, request, *args, **kwargs):
    #     context = getattr(request, "context_data", None) or {}
    #     # inline = context['inline_admin_formset'] # = context['inline_admin_formsets'].pop(0)
    #     return get_template(inline.opts.template).render(context, request)

    def get_form(self, request, obj=None, **kwargs):
        if request.user.is_superuser:
            kwargs['form'] = frm.FormNewProduct
        return super().get_form(request, obj, **kwargs)
    
    list_display = [
        'sku', 'featured_image_thumbnail','id','pim_code',
        'name','brand','unit','status','ps_overal_dimension','moq',
        'drawing_3d_dwg','drawing_3d_obj','drawing_3d_3dmax',
        'drawing_3d_sketchup',#'specification_image_inline'
    ]
    readonly_fields = (
        'id','pim_code',
        'featured_image_preview',
        # 'barcode_preview'
        #
    )
    search_fields = ['name','sku']
    list_filter = [
        'prefix_code',
        'category',
        'channel',
        'brand',
        'status',
        ]
    
    
    fieldsets = [
        (
            'General Information',{
            'fields':(
                'id','prefix_code','pim_code','sku',
                'name','brand','status','featured_image',
                # 'featured_image_thumbnail','image_preview',
                'featured_image_preview',
                'material','unit', 'channel', 'category', 'cost_price',
                # 'barcode_preview'
            )
        }),
        
        ('Product Specification',{
            'fields':(
                'ps_overal_dimension','ps_arm_height','ps_seat_height',
                'ps_seat_depth', 'ps_nett_weight', 'ps_gross_weight',
                'ps_product_type','ps_seat_construction' 
            )
        }),
        ('Shipping Details',{
            'fields':(
                'ps_box_dimension','ps_box_weight', 'ps_pax',
                'ps_20ft_container','ps_40gp_container',
                'ps_40hq_container', 'cbm', 'moq',  
            )
        }),
        ('Factory Drawing',{
            'fields':(
                'production_drawing_pdf', 'production_drawing_archive',
                'assembly_pdf','assembly_archive', 'bom_file'
            )
        }),
        ('Dezign Studio',{
            'fields':(
                'drawing_3d_dwg','drawing_3d_obj','drawing_3d_3dmax',
                'drawing_3d_sketchup'
            )
        }),
        ('SEO',{
            'fields':(
                'seo_meta_title','seo_meta_description',
                'seo_meta_keyword','seo_content_overview'
            )
        }),

        
    ]
    change_form_template = 'admin/custom_change_form.html'
    change_list_template = 'admin/custom_change_list.html'
    list_per_page = 10
    inlines = [
        AmbienceImageInline,
        SpecificationImageInline,
        TechnicalImageInline,
     ]
    
    
    

# --------------Item category & Unit ----------------------
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['id','name']

# ---- Product details: ProductType, SeatConstruction, Pax --------
# ----------  Image --------------------
@admin.register(SpecificationImage)
@admin_thumbnails.thumbnail('image','Thumbnail')
class SpecificationImageAdmin(admin.ModelAdmin):

    @admin.display(description='Specification image display')
    def specification_image_preview(self, obj):
        return format_html('<img src="{}" style="max-width:500px; max-height:500px"/>'.format(obj.image.url))
    
    list_display = ['product','image', 'image_thumbnail']
    readonly_fields = ('specification_image_preview',)
    fieldset = [
        (None,{
            'fields':('product',
                        'image',
                        # 'featured_image_thumbnail',
                        # 'image_preview',
                        'specification_image_preview',
                       )
        }),
        ]

@admin.register(TechnicalImage)
@admin_thumbnails.thumbnail('image','Thumbnail')
class TechnicalImageAdmin(admin.ModelAdmin):

    @admin.display(description='Technical image display')
    def technical_image_preview(self, obj):
        return format_html('<img src="{}" style="max-width:500px; max-height:500px"/>'.format(obj.image.url))
    
    list_display = [ 'product','image_thumbnail']
    readonly_fields = ('technical_image_preview',)
    fieldset = [
        (None,{
            'fields':('product',
                        'image',
                        # 'featured_image_thumbnail',
                        # 'image_preview',
                        'technical_image_preview',
                       )
        }),
        ]
    

@admin.register(AmbienceImage)
@admin_thumbnails.thumbnail('image','Thumbnail')
class AmbienceImageAdmin(admin.ModelAdmin):

    @admin.display(description='Ambience image display')
    def ambience_image_preview(self, obj):
        return format_html('<img src="{}" style="max-width:500px; max-height:500px"/>'.format(obj.image.url))
    list_display = ['product', 'image_thumbnail']
    readonly_fields = ('ambience_image_preview',)
    fieldset = [
        (None,{
            'fields':('product',
                        'image',
                        # 'featured_image_thumbnail',
                        # 'image_preview',
                        'ambience_image_preview',
                       )
        }),
        ]

# @admin.register(Retailer)
# class RetailerAdmin(admin.ModelAdmin):
#     list_display = ['name', 'brand']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['id','name']