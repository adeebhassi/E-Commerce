from django.urls import path

from .views import *

name='Products'
urlpatterns = [
    path('single-product/<int:id>',singleProduct,name='singleProduct'),
    path('admin/get_subcategories/', get_subcategories, name='get_subcategories'),
    path('shop-list',shoplist,name='shoplist'),
    path('shop-list/<int:category_id>/',shoplistByCategory,name='shoplistByCategory'),
    path('add_to_wishlist',add_to_wishlist,name='add_to_wishlist'),
    path('wishlist',wishlistView,name='wishlist'),
    path('remove_item/<int:item_id>',remove_from_wishlist,name='removeitem'),
    path('cart',view_cart,name='view_cart'),
    path('add_to_cart/<int:id>',add_to_cart,name='add_to_cart'),
    path('cart_remove/<int:item_id>',remove_from_cart,name='remove_from_cart'),
    
]
