from django.db import models

# Create your models here.




# class Product(models.Model):
#     uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
#     store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
#     name = models.CharField(max_length=999)
#     description = models.TextField(max_length=999)
#     price = models.FloatField()
#     image = models.ImageField(upload_to='product_images/', null=True, blank=True)

#     sku = models.CharField(max_length=999)
#     bar_code = models.CharField(max_length=999)
    

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     is_blocked = models.BooleanField(default=False)
 
#     def __str__(self):
#         return self.name