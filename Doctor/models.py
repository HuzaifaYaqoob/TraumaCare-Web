from django.db import models

from django.utils.timezone import now, localtime


# Create your models here.

from Authentication.models import User
from Profile.models import Profile
from uuid import uuid4
from Trauma.models import Speciality, Disease
from Hospital.models import Hospital, HospitalLocation

from datetime import timedelta, datetime




AVAILABILITY_TEXT = {
    '24_HOURS_OPEN' : '24 Hours Open',
    'AVAILABILITY_TIME_SLOTS' : 'Available on Timeslots',
}

class Doctor(models.Model):

    AVAILABILITY_CHOICES = (
        ('24_HOURS_OPEN', '24_HOURS_OPEN'),
        ('AVAILABILITY_TIME_SLOTS', 'AVAILABILITY_TIME_SLOTS'),
    )


    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    user = models.ForeignKey(User, related_name='doctors', on_delete=models.PROTECT)
    profile = models.ForeignKey(Profile, related_name='profile_doctors', on_delete=models.PROTECT)

    email = models.CharField(max_length=700, default='')
    name = models.CharField(max_length=600, default='')
    heading = models.CharField(max_length=700, default='')

    dial_code = models.CharField(max_length=20, default='')
    mobile_number = models.CharField(max_length=20, default='', verbose_name='Doctor Personal Number')

    working_since = models.DateField()

    online_availability = models.CharField(choices=AVAILABILITY_CHOICES, default='24_HOURS_OPEN', max_length=100)

    desc = models.TextField(default='')

    slug = models.CharField(max_length=999, default='')

    is_approved = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    is_recommended = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now=now)


    def __str__(self):
        return f'{str(self.id)} -- {self.name}'
    
    @property
    def phone_number(self):
        if self.dial_code and self.mobile_number:
            return f'+{self.dial_code}-{self.mobile_number}'
    
        return ''
    

    @property
    def get_availability_text(self):
        availability = AVAILABILITY_TEXT.get(self.online_availability or '24_HOURS_OPEN')
        return availability
    
    def get_specialities(self,):
        return Speciality.objects.filter(
            speciality_doctorspecialities__doctor = self,
            speciality_doctorspecialities__is_deleted = False,
            speciality_doctorspecialities__is_active = True,
        )
    
    def get_diseases(self,):
        return Disease.objects.filter(
            disease_doctor_disease_specialities__doctor = self,
            disease_doctor_disease_specialities__is_deleted = False,
            disease_doctor_disease_specialities__is_active = True,
        )

    @property
    def specialities(self):
        return self.get_specialities()

    @property
    def diseases(self):
        return self.get_diseases()
    
    @property
    def profile_image(self):
        try:
            profile_pic = DoctorMedia.objects.get(
                doctor = self,
                file_type = 'Profile Image',
                is_deleted = False,
                is_active = True
            )
        except:
            return None
        else:
            if profile_pic.file:
                return profile_pic.file.url
            return None
    
    @property
    def years_of_experience(self):
        if self.working_since:
            return now().year - self.working_since.year
        
    

    def get_doctor_rating_percentage(self, reviews=None):
        if reviews:
            doctor_reviews = reviews
        else:
            doctor_reviews = DoctorReview.objects.filter(doctor = self, is_deleted = False, is_active=True)
        if doctor_reviews.exists():
            return int((sum(doctor_reviews.values_list('rating', flat=True)) / len(doctor_reviews)) / 5 * 100)
        else:
            return 100
        
    @property
    def fee_range(self):
        fees = DoctorTimeSlots.objects.filter(doctor = self)
        # .distinct('fee')
        if len(fees):
            fees = [int((fee.fee * (100 - (fee.discount))) / 100) if fee.discount else fee.fee for fee in fees]
            return [min(fees), max(fees)]
        return None

    @property
    def get_time_inverval(self):
        return 20
    

    @property
    def is_available_today(self):
        today = datetime.now()
        slots = DoctorTimeSlots.objects.filter(
            doctor = self,
            day__day = today.strftime('%A'),
            end_time__gte = today.time(),
            is_deleted = False,
            is_active = True
        ).order_by('start_time')
        if slots.exists():
            return slots[0]
        return False

    
    def save(self, *args, **kwargs):
        name = self.name
        name = name.replace(' ', '-').replace('/', '-').replace('--', '-')
        name = name.lower()
        if not self.mobile_number:
            self.dial_code = self.user.dial_code
            self.mobile_number = self.user.mobile_number
            
        self.slug = f'{name}-{self.id}'
        super(Doctor, self).save(*args, **kwargs)
    
    class Meta:
        permissions = [
            ("can_view_task", "Can view task"),
            ("can_edit_task", "Can edit task"),
            ("can_delete_task", "Can delete task"),
        ]



class DoctorMediaManager(models.Manager):

    def bulk_create(self, objs, **kwargs):
        blk_create = super(models.Manager,self).bulk_create(objs,**kwargs)
        for instance in objs:
            models.signals.post_save.send(instance.__class__, instance=instance, created=True)
        return blk_create
    

class DoctorMedia(models.Model):
    objects = DoctorMediaManager()


    DOCTOR_MEDIA_TYPES = (
        ('Profile Image', 'Profile Image'),
        ('CNIC Front', 'CNIC Front'),
        ('CNIC Back', 'CNIC Back'),
        ('License', 'License'),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_medias')

    file_type = models.CharField(choices=DOCTOR_MEDIA_TYPES, default='Profile Image',max_length=30)
    file = models.FileField(upload_to='Doctor/Files/%Y-%m')

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return f'{str(self.id)} -- '


class DoctorSpeciality(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_specialities')
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, null=True, related_name='speciality_doctorspecialities')


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return f'{self.speciality.name}'

class DoctorDiseasesSpeciality(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_disease_specialities')
    disease = models.ForeignKey(Disease, on_delete=models.SET_NULL, null=True, related_name='disease_doctor_disease_specialities')


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return f'{str(self.id)} -- '


class DoctorOnlineAvailability(models.Model):
    
    """
        This Table will be used for Doctor Availability with Hospital & Online
    """
    DAYS_CHOICES = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_available_days')


    day = models.CharField(choices=DAYS_CHOICES, default='Monday', max_length=20)


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)

    class Meta:
        verbose_name = 'Doctor Available Days'

    def __str__(self):
        return f'{self.day} -- Dr. {self.doctor.name}'

class Doctor24By7(models.Model):
    """
        This Table will be used if Doctor is available in case of Emergency. and How much He/She will charge.
        This Model should be OneToOne, Single instance against single Doctor
    """
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_24_availability')

    fee = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    service_fee = models.PositiveIntegerField(default=0, verbose_name='TraumaCare Service FEE in Percentage')

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)

    class Meta:
        verbose_name = 'Doctor Availability in Emergency'

    def __str__(self):
        return f'{str(self.id)} -- '


class DoctorWithHospital(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_hospital_timeslots')
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, null=True, blank=True, related_name='hospital_timeslots')
    location = models.ForeignKey(HospitalLocation, on_delete=models.PROTECT, null=True, blank=True, related_name='location_timeslots')

    phone = models.CharField(max_length=999, default='')


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_hospital_informed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True, null=True)


    @property
    def available_days(self):
        return DoctorTimeSlots.objects.filter(doc_hospital = self, is_deleted=False, is_active=True)
    
    @property
    def highest_discount_day(self):
        return DoctorTimeSlots.objects.filter(doc_hospital = self, is_deleted=False, is_active=True).order_by('discount').last()
    
    @property
    def next_availability(self):
        data = {}
        day_count = 0
        found = False
        today = datetime.now()
        today_day = today.strftime('%A')

        while not found:
            now_day = today + timedelta(days=day_count)
            today_available = DoctorTimeSlots.objects.filter(doc_hospital = self, day__day = now_day.strftime('%A'), is_deleted=False, is_active=True).order_by('start_time')
            if today_available:
                if day_count == 0:
                    data['label'] = 'Available Today'
                elif day_count == 1:
                    data['label'] = 'Available Tomorrow'
                else:
                    data['slot_date'] = f'{now_day.strftime("%A")} {now_day.strftime("%d/%m/%Y")}'
                    data['label'] = f'Next Available in {day_count} Days'

                NewOnlineAva = []
                for onava in today_available:
                    available_intervals = onava.slots_interval
                    if len(available_intervals) > 0:
                        onava.model_slots_intervals = available_intervals
                        NewOnlineAva.append(onava)

                data['slots'] = NewOnlineAva
                data['day_count'] = day_count
                data['day_date'] = now_day.strftime('%Y-%m-%d')
                if len(NewOnlineAva) > 0 or day_count >= 7 :
                    found = True 
                else:
                    day_count = day_count + 1
            else:
                day_count = day_count + 1

        return data

    def __str__(self):
        return f'Dr. {self.doctor.name} Available in {self.hospital.name} at {self.location.name}'

class DoctorTimeSlots(models.Model):
    AVAILABILITY_TYPE = (
        ('Online', 'Online'),
        ('Hospital', 'Hospital'),
    )
    """
        Time Slots Table for Doctor, This Table is for Doctor Online Availability except 24/7,
        This Table also be used for Doctor Availability with Hospital
        ~ If Availability type is Online, It's mean this Object/Record is for Online Availability. Then doc_hospital Field will be Null
        ~ If Availability type is Hospital, It's mean this Object/Record is for Hospital Availability. Then doc_hospital Field will be not Null
    """
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=None, related_name='doctor_timeslots')

    doc_hospital = models.ForeignKey(DoctorWithHospital, on_delete=models.CASCADE, null=True, blank=True, related_name='doc_hospital_timeslots')
    day = models.ForeignKey(DoctorOnlineAvailability, on_delete=models.CASCADE, related_name='day_timeslots')

    title = models.CharField(max_length=999, default='')
    start_time = models.TimeField()
    end_time = models.TimeField()
    fee = models.PositiveIntegerField(default=0)
    discount = models.PositiveIntegerField(default=0)
    service_fee = models.PositiveIntegerField(default=0, verbose_name='TraumaCare Service FEE in Percentage')

    availability_type = models.CharField(choices=AVAILABILITY_TYPE, default='Online', max_length=20)


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)

    class Meta:
        verbose_name = 'Doctor Availability + Fee (Hospital | Online)'
    

    @property
    def start_time_formated(self):
        if self.start_time:
            return self.start_time.strftime('%I:%M %p')
    
    @property
    def end_time_formated(self):
        if self.end_time:
            return self.end_time.strftime('%I:%M %p')
    
    @property
    def day_abbr(self):
        if self.day:
            return self.day.day.replace('day', '')
        

    @property
    def final_price(self):
        if self.discount:
            return int(self.fee - (self.discount / 100) * self.fee)
        return self.fee
    

    @property
    def slots_interval(self):
        time_now = datetime.now()
        time_now = time_now.time()
        start_time = datetime.strptime(self.start_time.strftime("%H:%M"), "%H:%M")
        end_time = datetime.strptime(self.end_time.strftime("%H:%M"), "%H:%M")
        interval = timedelta(minutes=self.doctor.get_time_inverval)
        times = []
        current_time = start_time
        while current_time < end_time:
            if current_time.time() > time_now or self.slot_next_date['day_count'] > 0:
                times.append([current_time.strftime("%H:%M:00"), current_time.strftime("%I:%M %p")])
            current_time += interval

        return times

        
    @property
    def get_all_intervals(self):
        start_time = datetime.strptime(self.start_time.strftime("%H:%M"), "%H:%M")
        end_time = datetime.strptime(self.end_time.strftime("%H:%M"), "%H:%M")
        interval = timedelta(minutes=self.doctor.get_time_inverval)
        times = []
        current_time = start_time
        while current_time < end_time:
            times.append([current_time.strftime("%H:%M:00"), current_time.strftime("%I:%M %p")])
            current_time += interval

        return times
    

    @property
    def slot_next_date(self):
        data = {}
        day_count = 0
        found = False
        today = datetime.now()
        today_day = today.strftime('%A')

        while not found:
            now_day = today + timedelta(days=day_count)
            now_day_name = now_day.strftime('%A')
            if now_day_name == self.day.day:
                if day_count == 0:
                    data['label'] = 'Available Today'
                elif day_count == 1:
                    data['label'] = 'Available Tomorrow'
                else:
                    data['slot_date'] = f'{now_day_name} {now_day.strftime("%d/%m/%Y")}'
                    data['label'] = f'Next Available in {day_count} Days'
                
                data['day_count'] = day_count
                data['day_date'] = now_day.strftime('%Y-%m-%d')
                found = True
            else:
                day_count = day_count + 1

        return data
    

    def save(self, *args, **kwargs):
        if not self.service_fee:
            if self.doc_hospital:
                self.service_fee = self.doc_hospital.hospital.fee

        super(DoctorTimeSlots, self).save(*args, **kwargs)
    

    def __str__(self):
        return f'{str(self.id)} -- '

class DoctorEducation(models.Model):
    DEGREE_TYPE_CHOICES = (
        ('Master', 'Master'),
        ('MBBS', 'MBBS'),
        ('MD', 'MD'),
        ('Diploma', 'Diploma'),
        ('Other', 'Other'),
    )
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_education')

    degree_name = models.CharField(max_length=999, default='')
    degree_type = models.CharField(max_length=999, default='', choices=DEGREE_TYPE_CHOICES)
    speciality = models.CharField(max_length=999, default='')
    institute = models.CharField(max_length=999, default='')

    docs = models.FileField(upload_to='doctor_education/docs/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return f'{str(self.id)} -- Dr. {self.doctor.name}'


class DoctorExperience(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_experiences')

    speciality = models.CharField(max_length=999, default='')
    practice_institute = models.CharField(max_length=999, default='')

    docs = models.FileField(upload_to='doctor_experience/docs/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=now)
    updated_at = models.DateTimeField(auto_now_add=now)


    def __str__(self):
        return f'{str(self.id)} -- Dr. {self.doctor.name}'


class DoctorReview(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviews')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_reviews')
    review = models.TextField(default='')


    rating = models.PositiveIntegerField(default=0, ) # This rating won't related to Customer Input. We'll SUM Recommende, Checkup, Clinical Environment, Staff Behaviour and divide by 4 and save it as Rating.
    recommended_rating = models.PositiveIntegerField(default=0)
    checkup_rating = models.PositiveIntegerField(default=0)
    clinical_environment_rating = models.PositiveIntegerField(default=0)
    staff_behaviour_rating = models.PositiveIntegerField(default=0)

    secret_review = models.TextField(default='')


    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=now)


class DoctorQuery(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_queries')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_queries')
    question = models.TextField(default='')
    answer = models.TextField(default='')

    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=now)

    def __str__(self):
        return f'{str(self.id)}'