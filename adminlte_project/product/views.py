from django.shortcuts import render, redirect
from .models import Product
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
            product = form.save(commit=False)
            category_list = request.POST.getlist('category')
            if category_list:
                # product.save()
                product.category.set(category_list)
            brand = request.POST.get('brand')
            if brand:
                product.brand = Brand.objects.get(id=brand)
            cost_price = request.POST.get('cost_price')
            if cost_price:
                product.cost_price = cost_price
            product.save()
            form.save_m2m()
            messages.success(request, 'Product was created successfully!')
            return redirect('/product/product-list')
        else:
            form = ProductForm()
            # return render(request, 'product/product_create.html', {'form': form})
    if request.method == 'GET':
        form = ProductForm()
        return render(request, 'product/product_create.html', {'form': form})
    

@login_required
def product_edit(request, id):
    product = Product.objects.get(id=id)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product was updated successfully!')
            return redirect('product_list')
    return render(request, 'product_edit.html', {'form': form, 'id': id})

@login_required
def product_delete(request, id):
    Product.objects.filter(id=id).delete()
    messages.warning(request, 'Product was deleted successfully!')
    return redirect('/product-list')

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
