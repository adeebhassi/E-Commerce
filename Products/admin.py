from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display=['name']
admin.site.register(Category,CategoryAdmin)

class SubCategoryAdmin(admin.ModelAdmin):
    list_display=['name','main_category']  
admin.site.register(SubCategory,SubCategoryAdmin)

class detailCategoryAdmin(admin.ModelAdmin):
    list_display=['name','sub_category']
admin.site.register(DetailCategory,detailCategoryAdmin)

class ImageInline(admin.TabularInline):
    model = Image
    extra=2

class VariantInline(admin.TabularInline):
    model = Variant
    extra=2
    

    
class ProductAdmin(admin.ModelAdmin):
    list_display=['name','price','detail_category','price','discount','discountedPrice']
    inlines=[ImageInline,VariantInline]
    
admin.site.register(Product,ProductAdmin)
admin.site.register(Variant)
admin.site.register(VariantValue)
admin.site.register(Variantion)
admin.site.register(Brand)
admin.site.register(Discount)
admin.site.register(Wishlist)
admin.site.register(CartItem)