from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
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


class User(AbstractBaseUser):
    SOCIAL_PLATFORM_CHOICES = [
        ('Google', 'Google'),
        ('Facebook', 'Facebook'),
        ('Twitter', 'Twitter'),
        ('Apple', 'Apple'),
    ]
    # Required Fields

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128, null=True, blank=True)

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
        return self.username

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True

    def get_all_permissions(self, user=None):
        return []

    
    def country_name(self):
        if self.country:
            return self.country.name
    
    @property
    def profiles(self):
        user_profiles = self.user_profiles.all()
        # .filter(profile_type = 'Patient')
        return user_profiles
    

    def save(self, *args, **kwargs):
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
        try:
            general_profile = Profile.objects.get(
                user = self,
                profile_type = 'Patient'
            )
        except:
            return None
        else:
            return general_profile.image_full_path
    
    @property
    def has_doctor_profile(self):
        from Doctor.models import Doctor
        try:
            Doctor.objects.get(
                user = self,
                is_active = True,
                is_deleted = False,
                is_blocked = False,
            )
        except Exception as err:
            return False
        else:
            return True
    

    @property
    def full_name(self):
        if self.first_name:
            return f'{self.first_name} {self.last_name if self.last_name else ""}'
        else :
            self.username


    # def account_type(self):
    #     return self.user_account_type.account_type

    class Meta:
        unique_together = ['dial_code', 'mobile_number']
