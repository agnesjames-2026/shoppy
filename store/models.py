
from django.db import models
from category.models import category
from django.urls import reverse


class product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse(
            'product_detail',
            args=[self.category.slug, self.slug]
        )

#Product Variation


class ProductVariation(models.Model):

    product = models.ForeignKey(
        product,
        on_delete=models.CASCADE,
        related_name='variations'
    )

    color = models.CharField(
        max_length=50,
        blank=True,
        default=''
    )

    size = models.CharField(
        max_length=20,
        blank=True,
        default=''
    )

    stock = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['product', 'color', 'size'],
                name='unique_product_color_size'
            )
        ]

    def __str__(self):
        variation_name = ' - '.join(
            value for value in [self.color, self.size] if value
        )

        return f"{self.product.product_name} - {variation_name or 'Default'}"
