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
    path('product-list', (views.product_list), name='product_list'),
    path('product-create', (views.product_create), name='product_create'),
    path('product-edit/<int:id>/', (views.product_edit), name='product_edit'),
    path('product-delete/<int:id>', (views.product_delete), name='product_delete'),
    ]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)