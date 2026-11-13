
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import product,ProductVariation
from category.models import category
from carts.models import Cart, CartItem
from django.db.models import Q

# ==========================================
# STORE PAGE WITH PAGINATION
# ==========================================


def store(request, category_slug=None):

    categories = None

    if category_slug is not None:
        categories = get_object_or_404(
            category,
            slug=category_slug
        )

        products = product.objects.filter(
            category=categories,
            is_available=True
        )
    else:
        products = product.objects.filter(
            is_available=True
        )

    # SEARCH FUNCTIONALITY
    keyword = request.GET.get('keyword', '').strip()

    if keyword:
        products = products.filter(
            Q(product_name__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    # Count filtered products
    product_count = products.count()

    # PAGINATION
    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    # Categories for sidebar
    links = category.objects.all()

    context = {
        'products': paged_products,
        'product_count': product_count,
        'links': links,
        'keyword': keyword,
    }

    return render(request, 'store/store.html', context)



# ==========================================
# PRODUCT DETAIL PAGE
# ==========================================


# ==========================================
# PRODUCT DETAIL PAGE
# ==========================================


def product_detail(request, category_slug, product_slug):

    single_product = get_object_or_404(
        product,
        category__slug=category_slug,
        slug=product_slug,
        is_available=True
    )

    # Get all variations for this product
    all_variations = ProductVariation.objects.filter(
        product=single_product
    )

    # Check whether this product has variations
    has_variations = all_variations.exists()

    # Get active variations that have stock
    variations = all_variations.filter(
        is_active=True,
        stock__gt=0
    )

    # Get available sizes
    sizes = variations.exclude(
        size=''
    ).values_list('size', flat=True).distinct()

    # Get available colors
    colors = variations.exclude(
        color=''
    ).values_list('color', flat=True).distinct()

    # Check whether product is already in cart
    in_cart = False

    if request.session.session_key:

        try:
            cart_obj = Cart.objects.get(
                cart_id=request.session.session_key
            )

            in_cart = CartItem.objects.filter(
                cart=cart_obj,
                product=single_product,
                is_active=True
            ).exists()

        except Cart.DoesNotExist:
            pass

    # Pass all required data to template
    context = {
        'single_product': single_product,
        'in_cart': in_cart,
        'has_variations': has_variations,
        'variations': variations,
        'sizes': sizes,
        'colors': colors,
    }

    return render(
        request,
        'store/product_detail.html',
        context
    )

