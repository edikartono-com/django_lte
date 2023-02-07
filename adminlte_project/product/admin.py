from django.contrib import admin

# # Register your models here.
from .models import *

# # Register your models here.
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(AmbienceImage)