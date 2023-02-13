from django.db import models

# Create your models here.


from uuid import uuid4

class Speciality(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    name = models.CharField(max_length=500, default='')
    svg_icon = models.TextField()
    color_code = models.CharField(max_length=10, default='')

    image = models.ImageField(upload_to='specialities/images/', null=True, blank=True)

    rank = models.IntegerField(default=1)

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    
    class Meta:
        verbose_name = 'Specility'
        verbose_name_plural = 'Specilities'