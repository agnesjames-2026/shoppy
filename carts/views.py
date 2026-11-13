
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db import transaction

from store.models import product, ProductVariation
from .models import Cart, CartItem


# ==========================================
# GET CART SESSION ID
# ==========================================

def _cart_id(request):

    cart = request.session.session_key

    if not cart:
        request.session.create()
        cart = request.session.session_key

    return cart


# ==========================================
# GET OR CREATE CART
# ==========================================

def _get_cart(request):

    cart, created = Cart.objects.get_or_create(
        cart_id=_cart_id(request)
    )

    return cart


# ==========================================
# GET AVAILABLE STOCK FOR CART ITEM
# ==========================================

def _get_available_stock(cart_item):

    if cart_item.variation:
        return cart_item.variation.stock

    return cart_item.product.stock


# ==========================================
# ADD PRODUCT TO CART
# ==========================================

@require_POST
@transaction.atomic
def add_cart(request, product_id):

    product_item = get_object_or_404(
        product,
        id=product_id,
        is_available=True
    )

    cart = _get_cart(request)

    # Check whether this product has active variations
    has_variations = ProductVariation.objects.filter(
        product=product_item,
        is_active=True
    ).exists()

    variation = None

    if has_variations:

        selected_size = request.POST.get('size', '').strip()
        selected_color = request.POST.get('color', '').strip()

        try:
            variation = ProductVariation.objects.select_for_update().get(
                product=product_item,
                size=selected_size,
                color=selected_color,
                is_active=True
            )

        except ProductVariation.DoesNotExist:
            messages.error(
                request,
                'Please select a valid size and color combination.'
            )
            return redirect(product_item.get_url())

        available_stock = variation.stock

    else:

        available_stock = product_item.stock

    if available_stock <= 0:

        messages.error(
            request,
            'This product is out of stock.'
        )

        return redirect(product_item.get_url())

    # Find the exact cart item, including its variation
    cart_item = CartItem.objects.select_for_update().filter(
        cart=cart,
        product=product_item,
        variation=variation,
        is_active=True
    ).first()

    if cart_item:

        if cart_item.quantity >= available_stock:

            messages.error(
                request,
                'You cannot add more than the available stock.'
            )

            return redirect(product_item.get_url())

        cart_item.quantity += 1
        cart_item.save(update_fields=['quantity'])

    else:

        CartItem.objects.create(
            product=product_item,
            variation=variation,
            cart=cart,
            quantity=1,
            is_active=True
        )

    messages.success(
        request,
        'Product successfully added to your cart!'
    )

    return redirect(product_item.get_url())


# ==========================================
# DISPLAY CART AND CALCULATE TOTAL
# ==========================================

def cart(request):

    cart_items = []
    total = 0
    tax = 0
    grand_total = 0

    cart_obj = Cart.objects.filter(
        cart_id=_cart_id(request)
    ).first()

    if cart_obj:

        cart_items = CartItem.objects.filter(
            cart=cart_obj,
            is_active=True
        ).select_related(
            'product',
            'variation'
        )

        for item in cart_items:

            item.sub_total = item.product.price * item.quantity

            total += item.sub_total

        tax = round(total * 0.18, 2)

        grand_total = round(total + tax, 2)

    context = {
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }

    return render(request, 'store/cart.html', context)


# ==========================================
# INCREASE QUANTITY
# ==========================================

@require_POST
def increment_cart(request, item_id):

    cart = _get_cart(request)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart,
        is_active=True
    )

    available_stock = _get_available_stock(cart_item)

    if cart_item.quantity < available_stock:

        cart_item.quantity += 1
        cart_item.save(update_fields=['quantity'])

    else:

        messages.warning(
            request,
            'You have reached the available stock limit.'
        )

    return redirect('cart')


# ==========================================
# DECREASE QUANTITY
# ==========================================

@require_POST
def decrement_cart(request, item_id):

    cart = _get_cart(request)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart,
        is_active=True
    )

    if cart_item.quantity > 1:

        cart_item.quantity -= 1
        cart_item.save(update_fields=['quantity'])

    else:

        cart_item.delete()

    return redirect('cart')


# ==========================================
# UPDATE QUANTITY MANUALLY
# ==========================================

@require_POST
def update_cart(request, item_id):

    cart = _get_cart(request)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart,
        is_active=True
    )

    try:

        quantity = int(request.POST.get('quantity', 1))

    except (ValueError, TypeError):

        messages.error(request, 'Please enter a valid quantity.')
        return redirect('cart')

    available_stock = _get_available_stock(cart_item)

    if quantity <= 0:

        cart_item.delete()

    elif quantity <= available_stock:

        cart_item.quantity = quantity
        cart_item.save(update_fields=['quantity'])

    else:

        messages.error(
            request,
            f'Only {available_stock} items are available.'
        )

    return redirect('cart')


# ==========================================
# REMOVE CART ITEM
# ==========================================

@require_POST
def remove_cart(request, item_id):

    cart = _get_cart(request)

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart=cart,
        is_active=True
    )

    cart_item.delete()

    messages.success(
        request,
        'Item removed from your cart.'
    )

    return redirect('cart')
