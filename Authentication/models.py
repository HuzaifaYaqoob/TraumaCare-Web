from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
import uuid
from django.utils.timezone import now
# Create your models here.

from Trauma.models import Country


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    SOCIAL_PLATFORM_CHOICES = [
        ('Google', 'Google'),
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('Apple', 'Apple'),
    ]

    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    # Required Fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    full_name = models.CharField(max_length=999, default='')

    username = models.CharField(max_length=30, unique=True)

    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    email = models.EmailField(verbose_name="email", max_length=60, unique=True) #unique=True)
    is_email_verified = models.BooleanField(default=False)

    dial_code = models.CharField(max_length=5, null=True, blank=True )
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    is_mobile_verified = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    gender = models.CharField(max_length=999, null=True, blank=True, choices=GENDER_CHOICES)

    # maiden_name = models.CharField(max_length=128, null=True, blank=True)
    social_account = models.BooleanField(default=False)
    social_platform = models.CharField(max_length=32, choices=SOCIAL_PLATFORM_CHOICES, null=True, blank=True)
    social_id = models.CharField(max_length=128, default='', blank=True, null=True)


    joined_at = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Updated Date Time', null=True, blank=True)

    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyAccountManager()

    def __str__(self):
        return self.full_name

    def country_name(self):
        if self.country:
            return self.country.name
    
    @property
    def profiles(self):
        user_profiles = self.user_profiles.all()
        # .filter(profile_type = 'Patient')
        return user_profiles
    

    def save(self, *args, **kwargs):
        if not self.email:
            self.email = f'{self.username}@fake.traumacare.pk'
        if not self.country:
            try:
                country = Country.objects.get(name__iexact = 'pakistan', dial_code='92')
            except:
                pass
            else:
                self.country = country
                
        super(User, self).save(*args, **kwargs)
    
    @property
    def profile_image(self):
        from Profile.models import Profile
        general_profile = Profile.objects.filter(
            user = self,
            profile_type = 'Patient'
        ).first()
        if not general_profile:
            return 'https://ionicframework.com/docs/img/demos/avatar.svg'
        else:
            return general_profile.image_full_path or 'https://ionicframework.com/docs/img/demos/avatar.svg'
    
    @property
    def patient_profiles(self):
        user_profiles = self.user_profiles.filter(
            profile_type = 'Patient',
            is_active = True,
            is_deleted = False,
            is_blocked = False,
        )
        return user_profiles

    @property
    def has_doctor_profile(self):
        from Doctor.models import Doctor
        doc_profiles = Doctor.objects.filter(
            user = self,
            is_active = True,
            is_deleted = False,
            is_blocked = False,
        )
        if doc_profiles.exists():
            return True
        else:
            return False

    @property
    def has_hospital_profile(self):
        from Hospital.models import Hospital
        hos_profiles = Hospital.objects.filter(
            user = self,
            is_active = True,
            is_deleted = False,
            is_blocked = False,
        )
        if hos_profiles.exists():
            return True
        else:
            return False
    
    # def account_type(self):
    #     return self.user_account_type.account_type

    class Meta:
        unique_together = ['dial_code', 'mobile_number']

class Role(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
  
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='role_created_by')
    name = models.CharField(max_length=255, default='')
    description = models.TextField(blank=True, null=True)  # Optional description of the role

    rank = models.IntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True, related_name='child_roles')

    slug = models.TextField(default=uuid.uuid4)

    status = models.CharField(max_length=255, default='Active', choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        name = self.name
        name = name.replace(' ', '-').lower()
        self.slug = name
        super(Role, self).save(*args, **kwargs)

    def __str__(self):
        return f'({self.rank}) {self.name}{f" >> {self.parent.name}" if self.parent else ""}'

    def get_child_roles(self):
        return Role.objects.filter(parent=self)
    
    def role_user(self):
        return User.objects.filter(user_roles__role=self, user_roles__is_active=True, is_active=True, is_deleted=False)

class StaffRole(models.Model):

    role = models.ManyToManyField(Role)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles', unique=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.full_name}'