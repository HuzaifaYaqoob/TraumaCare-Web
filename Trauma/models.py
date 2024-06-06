from django.db import models


# Create your models here.

from uuid import uuid4

class Speciality(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    name = models.CharField(max_length=500, default='')
    speciality_type = models.CharField(max_length=999, default='')
    svg_icon = models.TextField()
    color_code = models.CharField(max_length=10, default='')
    description = models.TextField(default='')

    image = models.ImageField(upload_to='specialities/images/', null=True, blank=True)

    slug = models.CharField(max_length=800, default='')
    tag_line = models.CharField(max_length=800, default='')

    rank = models.IntegerField(default=1)

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            name = self.name
            name = name.replace(' ', '-').replace('/', '-')
            self.slug = name
        
        super(Speciality, self).save(*args, **kwargs)

    @property
    def available_doctors_count(self):
        from Doctor.models import DoctorSpeciality
        return DoctorSpeciality.objects.filter(
            speciality = self,
            is_deleted = False,
            is_active = True
        ).count()
        # .distinct('doctor')

    @property
    def available_doctors(self):
        from Doctor.models import Doctor
        return Doctor.objects.filter(
            doctor_specialities__speciality = self,
            is_deleted = False,
            is_active = True
        )
        # .distinct('doctor')

    
    class Meta:
        verbose_name = 'Specility'
        verbose_name_plural = 'Specilities'

class Disease(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True, blank=True, related_name='speciality_diseases')

    name = models.CharField(max_length=500, default='')
    svg_icon = models.TextField()
    color_code = models.CharField(max_length=10, default='')
    description = models.TextField(default='')

    image = models.ImageField(upload_to='disease/images/', null=True, blank=True)

    slug = models.CharField(max_length=800, default='')
    tag_line = models.CharField(max_length=800, default='')

    rank = models.IntegerField(default=1)

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            name = self.name
            name = name.replace(' ', '-').replace('/', '-')
            self.slug = name
        
        super(Disease, self).save(*args, **kwargs)

    @property
    def available_doctors_count(self):
        from Doctor.models import DoctorDiseasesSpeciality
        return DoctorDiseasesSpeciality.objects.filter(
            disease = self,
            is_deleted = False,
            is_active = True
        ).count()
        # .distinct('doctor')
    
    class Meta:
        verbose_name = 'Disease'
        verbose_name_plural = 'Diseases'


class Country(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    name = models.CharField(max_length=500, default='')
    svg_icon = models.TextField()
    color_code = models.CharField(max_length=10, default='')
    description = models.TextField(default='')

    dial_code = models.CharField(default='', max_length=20)

    flag = models.ImageField(upload_to='country/flags/', null=True, blank=True)


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

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
        return f'{self.name} -- {self.country.name}'

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
        return f'{self.name} -- {self.state.name} -- {self.country.name}'

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'


class RandomFiles(models.Model):
    image = models.ImageField(upload_to='random_files/images/', null=True, blank=True)

    def __str__(self):
        return f'{self.id}'

class VerificationCode(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    user = models.ForeignKey('Authentication.User', on_delete=models.CASCADE, related_name='user_verification_codes')
    code = models.CharField(default='', max_length=50)

    otp_type = models.CharField(max_length=999, default='')

    is_expired = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    is_used = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'code',)

    def save(self, *args, **kwargs):
        if not self.code:
            import random
            random_id = ''.join([str(random.randint(0, 999)).zfill(3) for _ in range(2)])
            self.code = random_id

        super(VerificationCode, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.id}'

