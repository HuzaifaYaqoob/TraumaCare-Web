from django.contrib import admin
from django.db.models import Q, Count

from django.utils.html import mark_safe
from .models import Doctor, Doctor24By7, Leave, DoctorReview, DoctorQuery, DoctorEducation, DoctorExperience, DoctorWithHospital, DoctorDiseasesSpeciality, DoctorMedia, DoctorOnlineAvailability, DoctorSpeciality, DoctorTimeSlots, DoctorRequest

# Register your models here.

def get_label(text, color='#0755E9'):
    return f"""<span style="display:inline-block;font-size:11px !important;font-weight:400;padding:2px 5px;border-radius:5px;background-color:{color};color:white">{text}</span>"""

COLORS = ['#0755E9',"#05DC75",'#F01275',"#F8DB48",'#A737D5','Black','#0755E9',"#05DC75",'#F01275',"#F8DB48",'#A737D5','Black','#0755E9',"#05DC75",'#F01275',"#F8DB48",'#A737D5','Black']

class DoctorDiseasesSpecialityInline(admin.TabularInline):
    model = DoctorDiseasesSpeciality
    extra = 0

    raw_id_fields = [
        "disease"
    ]

class DoctorSpecialityInline(admin.TabularInline):
    model = DoctorSpeciality
    extra = 0

    raw_id_fields = [
        "speciality"
    ]

class DoctorMediaInline(admin.TabularInline):
    model = DoctorMedia
    extra = 0   

class DoctorWithHospitalInline(admin.StackedInline):
    model = DoctorWithHospital
    extra = 0
    raw_id_fields = [
        "hospital",
        "location",
    ]

class DoctorOnlineAvailabilityInline(admin.TabularInline):
    model = DoctorOnlineAvailability
    extra = 0

    fields = ['day', 'is_active', 'is_deleted']

class DoctorTimeSlotsInline(admin.StackedInline):
    model = DoctorTimeSlots
    extra = 0

    exclude = ['discount', 'service_fee']
    raw_id_fields = [
        "doc_hospital",
        "day",
    ]


class Doctor24By7Inline(admin.TabularInline):
    model = Doctor24By7
    extra = 0

class DoctorEducationInline(admin.TabularInline):
    model = DoctorEducation
    extra = 0

class DoctorExperienceInline(admin.TabularInline):
    model = DoctorExperience
    extra = 0

class DoctorReviewInline(admin.TabularInline):
    model = DoctorReview
    extra = 0

class DoctorQueryInline(admin.TabularInline):
    model = DoctorQuery
    extra = 0

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    list_display = [
        # 'email', 
        # 'slug', 
        'doctor', 
        # 'desc',
        # 'mobile_number', 
        'days', 
        'diseases', 
        'speciality', 
        'is_approved', 
        'is_active', 
        'is_deleted', 
        'is_blocked', 
        'is_featured', 
        'is_recommended',
        'created_at',
    ]
    search_fields = ['id', 'email', 'name', 'heading', 'mobile_number']

    inlines = [
        DoctorDiseasesSpecialityInline,
        DoctorSpecialityInline,
        DoctorMediaInline,
        DoctorWithHospitalInline,
        DoctorOnlineAvailabilityInline,
        DoctorTimeSlotsInline,
        # Doctor24By7Inline,
        # DoctorEducationInline,
        # DoctorExperienceInline,
        # DoctorReviewInline,
        # DoctorQueryInline,
    ]
    def get_exclude(self, request, obj=None):
        excluded_fields = ['slug', 'email', 'online_availability', 'dial_code']
        if obj and obj.pk:
            excluded_fields.extend(['user', 'profile'])
        return excluded_fields
    # exclude = [
    #     'slug',
    #     'email',
    #     'online_availability',
    #     'dial_code',
    # ]

    def doctor(self, d):
        labels = []
        for i, dh in enumerate(DoctorWithHospital.objects.filter(doctor = d, is_deleted = False, is_active = True).values_list('hospital__name', flat=True)):
            labels.append(get_label(dh, color=COLORS[i]))
        
        return d.doctor_admin_card(labels=labels)

    
    def diseases(self, doctor_instance):
        return DoctorDiseasesSpeciality.objects.filter(
            doctor = doctor_instance
        ).count()
    
    def speciality(self, doctor_instance):
        return DoctorSpeciality.objects.filter(
            doctor = doctor_instance,
            is_deleted = False,
            is_active = True,
        ).count()
    
    def days(self, doctor):
        return DoctorOnlineAvailability.objects.filter(doctor = doctor, is_active = True, is_deleted=False).count()
    days.admin_order_field = 'days'


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(days = Count('doctor_available_days', Where = Q(doctor_available_days__is_active = True, doctor_available_days__is_deleted=False)))



@admin.register(Doctor24By7)
class Doctor24By7Admin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DoctorDiseasesSpeciality)
class DoctorDiseasesSpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor', 'disease']


@admin.register(DoctorMedia)
class DoctorMediaAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DoctorOnlineAvailability)
class DoctorOnlineAvailabilityAdmin(admin.ModelAdmin):
    list_filter = [
        'doctor',
        'day',
        'is_active',
    ]
    search_fields = [
        'doctor__name',
        'day'
    ]
    list_display = [
        'doc',
        'day',
        'is_active',
        'is_deleted',
    ]

    @admin.display(description='Doctor')
    def doc(self, d):
        return d.doctor.doctor_admin_card()
    doc.admin_order_field = 'doctor'


@admin.register(DoctorSpeciality)
class DoctorSpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor', 'speciality']


@admin.register(DoctorTimeSlots)
class DoctorTimeSlotsAdmin(admin.ModelAdmin):
    ordering = ['doctor', 'doc_hospital', 'day__day', 'start_time']
    list_filter = [
        'doctor',
        'doc_hospital__hospital',
    ]
    list_display = [
        'doc',
        'hos',
        'available_day',
        'title',
        'start_time',
        'end_time',
        'fee',
        'discount',
        # 'service_fee',
        'is_active',
    ]

    @admin.display(description='Day')
    def available_day(self, d):
        return d.day.day
    available_day.admin_order_field = 'day'

    @admin.display(description='Doctor')
    def doc(self, d):
        return d.doctor.doctor_admin_card()
    doc.admin_order_field = 'doctor'

    @admin.display(description='Hospital')
    def hos(self, d):
        if d.doc_hospital:
            return d.doc_hospital.hospital.hospital_admin_card(tag_line=d.doc_hospital.location.name)
        return f'{d.availability_type} Slot'
    hos.admin_order_field = 'hospital'


@admin.register(DoctorReview)
class DoctorReviewAdmin(admin.ModelAdmin):
    list_display = ['id']


@admin.register(DoctorWithHospital)
class DoctorWithHospitalAdmin(admin.ModelAdmin):
    list_filter = [
        'doctor',
        'hospital',
        'is_active',
    ]
    list_display = [
        'doc',
        'hos',
        # 'location',
        'phone',
        'is_active',
    ]
    @admin.display(description='Doctor')
    def doc(self, d):
        return d.doctor.doctor_admin_card()
    doc.admin_order_field = 'doctor'

    @admin.display(description='Hospital')
    def hos(self, d):
        return d.hospital.hospital_admin_card(tag_line=d.location.street_address)
    hos.admin_order_field = 'hospital'


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_filter = [
        'doctor',
    ]
    list_display = [
        'doct',
        'start_date',
        'end_date',
        'is_active',
        'created_at',
    ]

    @admin.display(description='Doctor')
    def doct(self, leave_obj):
        return leave_obj.doctor.doctor_admin_card()
    doct.admin_order_field = 'doctor'

@admin.register(DoctorRequest)
class DoctorRequestAdmin(admin.ModelAdmin):
    search_fields = [
        'name', 'phone', 'speciality'
    ]
    list_filter = ['gender']
    ordering = ['-created_at', 'is_onboarded']
    list_display = ['name', 'phone', 'gender', 'speciality', 'is_onboarded', 'is_active', 'created_at']

@admin.register(DoctorEducation)
class DoctorEducationAdmin(admin.ModelAdmin):
    list_display = ['degree_name', 'is_active', 'created_at']