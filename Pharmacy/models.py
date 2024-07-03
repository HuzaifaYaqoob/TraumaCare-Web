# from django.db import models

# # Create your models here.



# from django.db import models



# class Store(models.Model): # Medical Store
#     uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
#     name = models.CharField(max_length=999)
#     logo = models.ImageField(upload_to='store_logo/', null=True, blank=True)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField(null=True, blank=True)
#     website = models.URLField(null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     is_blocked = models.BooleanField(default=False)
 
#     def __str__(self):
#         """
#             Return a string representation of the object.
#             Returns:
#                 str: The name of the object.
#         """
#         return self.name


# class StoreLocation(models.Model):
#     uuid = models.UUIDField(default=uuid4, editable=False, unique=True)
#     store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_locations')
#     name = models.CharField(max_length=999)
#     address = models.TextField(max_length=999)
#     phone = models.CharField(max_length=20)
#     email = models.EmailField(null=True, blank=True)
#     lat = models.CharField(max_length=999)
#     lng = models.CharField(max_length=999)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     is_active = models.BooleanField(default=True)
#     is_blocked = models.BooleanField(default=False)
 
#     def __str__(self):
#         return self.name


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