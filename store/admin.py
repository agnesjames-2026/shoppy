from django.contrib import admin
from .models import product,ProductVariation

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','category','created_date','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}
admin.site.register(product)
admin.site.register(ProductVariation)
# Register your models here.
