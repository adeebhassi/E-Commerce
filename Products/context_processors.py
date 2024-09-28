from .models import Category,CartItem,SubCategory,Product

def category_context(request):
    categories = Category.objects.all()
    subcategories=SubCategory.objects.all()
    products=Product.objects.all()
    print(subcategories)
    return {'categories': categories,'subcategories':subcategories,'products':products}


def cart_item_count(request):
    if request.user.is_authenticated:
        count = CartItem.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'cart_item_count': count}


def cart_item(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items=None
    return {'cart_item':cart_items}