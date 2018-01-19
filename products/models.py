from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    name_product = models.CharField(max_length=100, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "%s" % self.name_product

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категория товаров'

class Product(models.Model):
    # id_customer = models.AutoField(primary_key=True)
    name_product = models.CharField(max_length=100, blank=True, null=True, default=None)
    category = models.ForeignKey(ProductCategory,blank=True, null=True, default=None, on_delete=models.CASCADE)
    short_description = models.TextField(blank=True, null=True, default=None)
    price = models.IntegerField(blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "Товар %s, %s" % (self.name_product, self.price)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

class ProductIMG(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,blank=True, null=True, default=None)
    image = models.ImageField(upload_to='products_images/')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.id

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

