
from django.db import models
from store.models import product, ProductVariation


class Cart(models.Model):

    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):

    product = models.ForeignKey(
        product,
        on_delete=models.CASCADE
    )

    variation = models.ForeignKey(
        ProductVariation,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.product)
