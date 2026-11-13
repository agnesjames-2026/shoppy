
from django.db.models import Sum
from .models import Cart, CartItem


def counter(request):

    cart_count = 0

    # Don't calculate cart count in admin pages
    if request.path.startswith('/admin/'):
        return {}

    session_key = request.session.session_key

    if session_key:

        try:
            cart = Cart.objects.get(cart_id=session_key)

            result = CartItem.objects.filter(
                cart=cart,
                is_active=True
            ).aggregate(
                total_quantity=Sum('quantity')
            )

            cart_count = result['total_quantity'] or 0

        except Cart.DoesNotExist:
            cart_count = 0

    return {
        'cart_count': cart_count
    }
