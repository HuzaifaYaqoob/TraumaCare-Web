from django.db import models

# Create your models here.


class XpoKey(models.Model):
    key = models.TextField(default='')

    def __str__(self):
        return f'{self.id}'