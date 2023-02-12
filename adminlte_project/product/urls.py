from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# from django.contrib.auth.decorators import login_required

app_name = 'product'

urlpatterns = [
    # path('', views.product_list, name='product-list'),
    # path('create/', views.product_create, name='product-create'),
    # path('<int:pk>/update/', views.product_update, name='product-update'),
    # path('', views.index, name='index'),
    path('product-list/', views.product_list, name='product_list'),
    path('product-create/', views.product_create, name='product_create'),
    path('product-edit/<int:id>/', views.product_edit, name='product_edit'),
    path('product-delete/<int:id>', views.product_delete, name='product_delete'),
    path('category-list/', views.category_list, name='category_list'),
    path('category-create/', views.category_create, name='category_create'),
    path('category-edit/<int:id>/', views.category_edit, name='category_edit'),
    path('category-delete/<int:id>', views.category_delete, name='category_delete'),
    path('brand-list/', views.brand_list, name='brand_list'),
    path('brand-create/', views.brand_create, name='brand_create'),
    path('brand-edit/<int:id>/', views.brand_edit, name='brand_edit'),
    path('brand-delete/<int:id>', views.brand_delete, name='brand_delete'),
    path('ambienceimage-list/', views.ambienceimage_list, name='ambienceimage_list'),
    path('ambienceimage-create/', views.ambienceimage_create, name='ambienceimage_create'),
    path('ambienceimage-edit/<int:id>/', views.ambienceimage_edit, name='ambienceimage_edit'),
    path('ambienceimage-delete/<int:id>', views.ambienceimage_delete, name='ambienceimage_delete'),
    path('specificationimage-list/', views.specificationimage_list, name='specificationimage_list'),
    path('specificationimage-create/', views.specificationimage_create, name='specificationimage_create'),
    path('specificationimage-edit/<int:id>/', views.specificationimage_edit, name='specificationimage_edit'),
    path('specificationimage-delete/<int:id>', views.specificationimage_delete, name='specificationimage_delete'),
    path('technicalimage-list/', views.technicalimage_list, name='technicalimage_list'),
    path('technicalimage-create/', views.technicalimage_create, name='technicalimage_create'),
    path('technicalimage-edit/<int:id>/', views.technicalimage_edit, name='technicalimage_edit'),
    path('technicalimage-delete/<int:id>', views.technicalimage_delete, name='technicalimage_delete')

    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)