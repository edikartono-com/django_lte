from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Brand, Category, AmbienceImage
import datetime
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ProductForm, CategoryForm, BrandForm, AmbienceImageForm
from django.urls import reverse

# @login_required
# def index(request):
#     return render(request, 'index.html')
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product/product_list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                category_list = request.POST.getlist('category')
                brand = request.POST.get('brand')
                if brand:
                    product.brand, created = Brand.objects.get_or_create(id=brand)
                cost_price = request.POST.get('cost_price')
                if cost_price:
                    product.cost_price = cost_price
                product.save()
                if category_list:   
                    product.category.set(category_list)
                else:
                    product.category.clear()
                form.save_m2m()
                messages.success(request, 'Product was created successfully!')
                return redirect(reverse('product:product_list'))
                # return redirect('/product/product-list')
                # return render(request, 'product/product_edit.html', {'form': form})
            except Exception as e:
                messages.error(request, str(e))
                return render(request, 'product/product_create.html', {'form': form})
        else:
            # form = ProductForm()
            messages.error(request, 'Failed to create product!')
            return render(request, 'product/product_create.html', {'form': form})
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'product/product_create.html', {'form': form})
    

@login_required
def product_edit(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                product = form.save(commit=False)
                category_list = request.POST.getlist('category')
                brand = request.POST.get('brand')                
                if brand:
                    product.brand, created = Brand.objects.get_or_create(id=brand)
                cost_price = request.POST.get('cost_price')
                if cost_price:
                    product.cost_price = cost_price
                product.save()
                if category_list:   
                    product.category.set(category_list)
                else:
                    product.category.clear()
                form.save_m2m()
                messages.success(request, 'Product was updated successfully!')
                return redirect(reverse('product:product_edit', args=[product.id]))
            except Exception as e:
                messages.error(request, str(e))
                return render(request, 'product/product_edit.html', {'form': form, 'id': id})
        else:
            messages.error(request, 'Failed to update product!')
            return render(request, 'product/product_edit.html', {'form': form, 'id': id})
    if request.method == 'GET':
        form = ProductForm(instance=product)
        return render(request, 'product/product_edit.html', {'form': form, 'id': id})




@login_required
def product_delete(request, id):
    # Product.objects.filter(id=id).delete()
    product = get_object_or_404(Product, id=id)
    try:
        product.delete()
        messages.success(request, 'Product was deleted successfully!')
        return redirect('product:product_list')
    except Exception as e:
    # messages.warning(request, 'Product was deleted successfully!')
        messages.error(request, str(e))
    return redirect('product:product_list')

@login_required
def product_details(request, id):
    product = Product.objects.get(id=id)
    context = {'product': product}
    return render(request, 'product_details.html', context)

# @login_required
# def sample(request):
#     # product = Product.objects.get(id=id)
#     # context = {'product': product}
#     return render(request, 'sample.html')


# ==========================---CATEGORY---=====================
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'product/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product:category_list')
    else:
        form = CategoryForm()
    return render(request, 'product/category_create.html', {'form': form})

def category_edit(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('product:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'product/category_edit.html', {'form': form})

def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    category.delete()
    return redirect('product:category_list')

# ==========================---BRAND---=====================
def brand_list(request):
    brands = Brand.objects.all()
    return render(request, 'product/brand_list.html', {'brands': brands})

def brand_create(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product:brand_list')
    else:
        form = BrandForm()
    return render(request, 'product/brand_create.html', {'form': form})

def brand_edit(request, id):
    brand = get_object_or_404(Brand, id=id)
    if request.method == 'POST':
        form = BrandForm(request.POST, instance=brand)
        if form.is_valid():
            form.save()
            return redirect('product:brand_list')
    else:
        form = BrandForm(instance=brand)
    return render(request, 'product/brand_edit.html', {'form': form})

def brand_delete(request, id):
    brand = get_object_or_404(Brand, id=id)
    brand.delete()
    return redirect('product:brand_list')

# ==========================---AMBIENCE IMAGE---=====================
def ambienceimage_list(request):
    ambienceimages = AmbienceImage.objects.all()
    return render(request, 'ambienceimage/ambienceimage_list.html', {'ambienceimages': ambienceimages})

def ambienceimage_create(request):
    if request.method == 'POST':
        form = AmbienceImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('ambienceimage_list')
    else:
        form = AmbienceImageForm()
    return render(request, 'ambienceimage/ambienceimage_create.html', {'form': form})

def ambienceimage_edit(request, id):
    ambienceimage = get_object_or_404(AmbienceImage, id=id)
    if request.method == 'POST':
        form = AmbienceImageForm(request.POST, request.FILES, instance=ambienceimage)
        if form.is_valid():
            form.save()
            return redirect('ambienceimage_list')
    else:
        form = AmbienceImageForm(instance=ambienceimage)
    return render(request, 'ambienceimage/ambienceimage_edit.html', {'form': form})

def ambienceimage_delete(request, id):
    ambienceimage = get_object_or_404(AmbienceImage, id=id)
    ambienceimage.delete()
    return redirect('ambienceimage_list')