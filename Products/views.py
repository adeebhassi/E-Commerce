from django.shortcuts import render,redirect
from .models import Product,SubCategory,DetailCategory,Wishlist,CartItem
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.sites.models import Site
# Create your views here.


def index(request):
    products=Product.objects.all()
    context={
        'products':products
    }
    return render(request,'core/index-6.html',context)


@login_required
def singleProduct(request,id):
    product=Product.objects.get(id=id)
    images=product.images.all()
    variants=product.variants.all()
    variation_dict={}
    for variant in variants:
        variation_name=variant.value.variation.name
        value=variant.value.value
        if variation_name not in variation_dict:
            variation_dict[variation_name]=[]
        variation_dict[variation_name].append(value)
    context={
        'product':product,
        'images':images,
        'variations':variation_dict
    }
    return render(request,'core/shop-product-detail-left-sidebar.html',context)

def get_subcategories(request):
    category_id = request.GET.get('category_id')
    sub_category_id=request.GET.get('subCategory_id')
    
    response_data={
        'subcategories':[],
        'detailcategories':[]
    }
    if category_id:
        subcategories = SubCategory.objects.filter(main_category_id=category_id).values('id', 'name')
        response_data['subcategories']=list(subcategories)
    else:
        print("unable to get the id")
    if sub_category_id:
        detailcategores=DetailCategory.objects.filter(sub_category_id=sub_category_id).values('id','name')
        response_data['detailcategories']=list(detailcategores)
    print(response_data)
    return JsonResponse(response_data, safe=False)


def productListAJAX(request):
    products=Product.objects.filter().values_list('name',flat=True)
    productList=list(products)
    print(productList)
    return JsonResponse(productList,safe=False)

def searchProduct(request):
    if request.method=='POST':
        searchedTerm=request.POST.get('searchProduct')
        if searchedTerm=='':
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            product=Product.objects.filter(name__icontains=searchedTerm).first()
            if product:
                return redirect('singleProduct',id=product.id)
            else:
                messages.info(request,'Item not found ,try something else')
                return redirect(request.META.get('HTTP_REFERER'))
    return redirect(request.META.get('HTTP_REFERER'))



def shoplist(request,category_id=None):
    products = Product.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
        print(products)
    context={
        'products':products,
    }
    return render(request,'core/shop-list.html',context)

def shoplistByCategory(request,category_id):
    if category_id:
        products = Product.objects.filter(category_id=category_id)
        print(products)
    context={
        'products':products,
    }
    return render(request,'core/shop-list.html',context)


def add_to_wishlist(request):
    if request.method == "POST" and request.user.is_authenticated:
        product_id = request.POST.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        
        wishlist, created = Wishlist.objects.get_or_create(user=request.user, products=product)
        
        if created:
            return JsonResponse({'success': True, 'message': 'Added to wishlist!'})
        else:
            return JsonResponse({'success': False, 'message': 'Already in wishlist!'})
    return JsonResponse({'success': False, 'message': 'Invalid request!'})



def wishlistView(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist': wishlist,
        }
    return render(request, 'core/wishlist.html', context)


def remove_from_wishlist(request,item_id):
    item=Wishlist.objects.get(id=item_id)
    item.delete()
    wishlist = Wishlist.objects.filter(user=request.user)
    context = {
        'wishlist': wishlist,
        }
    return render(request, 'core/wishlist.html',context)

def view_cart(request):
    cart_item=CartItem.objects.filter(user=request.user)
    total_price=sum(item.product.price * item.quantity for item in cart_item)
    shiping_cost=1000
    grand_total=total_price + shiping_cost
    context={
        'cart_item':cart_item,
        'total_price':total_price,
        'grand_total':grand_total,
        'shiping_cost':shiping_cost
    }
    return render(request,'core/shop-cart.html',context)

def add_to_cart(request,id):
    product=Product.objects.get(id=id)
    cart_item,crearted=CartItem.objects.get_or_create(product=product,user=request.user)
    cart_item.quantity +=1
    cart_item.save()
    
    return redirect('view_cart')


def remove_from_cart(request,item_id):
    item=CartItem.objects.get(id=item_id)
    item.delete()
    print("item gone")
    return JsonResponse({'success': True}) 