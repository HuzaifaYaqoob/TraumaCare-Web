from django.db import models

# Create your models here.


from uuid import uuid4

class Category(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)