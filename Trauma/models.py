from django.db import models

# Create your models here.


from uuid import uuid4

class Speciality(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    name = models.CharField(max_length=500, default='')
    svg_icon = models.TextField()
    color_code = models.CharField(max_length=10, default='')
    description = models.TextField(default='')

    image = models.ImageField(upload_to='specialities/images/', null=True, blank=True)

    rank = models.IntegerField(default=1)

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    
    class Meta:
        verbose_name = 'Specility'
        verbose_name_plural = 'Specilities'

class Disease(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    name = models.CharField(max_length=500, default='')
    svg_icon = models.TextField()
    color_code = models.CharField(max_length=10, default='')
    description = models.TextField(default='')

    image = models.ImageField(upload_to='disease/images/', null=True, blank=True)

    rank = models.IntegerField(default=1)

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    
    class Meta:
        verbose_name = 'Disease'
        verbose_name_plural = 'Diseases'


class Country(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    name = models.CharField(max_length=500, default='')
    svg_icon = models.TextField()
    color_code = models.CharField(max_length=10, default='')
    description = models.TextField(default='')

    flag = models.ImageField(upload_to='country/flags/', null=True, blank=True)


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'

class State(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    name = models.CharField(max_length=500, default='')
    svg_icon = models.TextField()
    color_code = models.CharField(max_length=10, default='')
    description = models.TextField(default='')

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_states')


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

class City(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    name = models.CharField(max_length=500, default='')
    svg_icon = models.TextField()
    color_code = models.CharField(max_length=10, default='')
    description = models.TextField(default='')

    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_cities')
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='state_cities')

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'