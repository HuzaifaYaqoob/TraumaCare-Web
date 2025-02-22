



from django.core.management.base import BaseCommand

from django.conf import settings
from datetime import datetime, timedelta
import time
import re
import random
import json

from Authentication.models import User
from Profile.models import Profile

from Doctor.models import Doctor, DoctorReview, DoctorWithHospital, DoctorTimeSlots, DoctorEducation, DoctorDiseasesSpeciality, DoctorSpeciality, DoctorOnlineAvailability, DoctorService
from Hospital.models import Hospital, HospitalLocation
from Trauma.models import Speciality, Disease, City, Service

DAYS_ABBR = {
    'M' : 'Monday',
    'Tu' : 'Tuesday',
    'W' : 'Wednesday',
    'Th' : 'Thursday',
    'F' : 'Friday',
    'Sa' : 'Saturday',
    'Su' : 'Sunday',
}

# "M, Tu, W, Th, F, Sa"

class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def handle(self, *args, **options):
        # with open('https://traumacare.blr1.digitaloceanspaces.com/static/uniqueDoctors.json')

        doctors = Doctor.objects.filter(desc = '')
        for doctor in doctors:
            description = f"Dr. {doctor.name} is a dedicated {','.join([sp.name for sp in doctor.specialities[:4]])} with {doctor.years_of_experience} years of experience in {','.join([sp.name for sp in doctor.diseases[:4]])}. Passionate about patient care, {'He' if not doctor.user.gender or doctor.user.gender == 'Male' else 'She'} is committed to providing compassionate, evidence-based treatment. Dr. {doctor.name} practices at {','.join([h.hospital.name for h in doctor.doctor_hospital_timeslots.all()])} and is also available for online consultations. For appointments, call 03400193324."
            print(description)
            doctor.desc = description
            doctor.save()
        print(doctors.count())
        
        # total_users = User.objects.all().count()
        # counter = 0
        # Udata = {'available_days' : 0}
        # with open('Files/uniqueDoctors.json' , 'r') as input_file:
        #     reader = json.load(input_file)
        #     for doctor_id, doctor_obj in reader.items():
        #         # print(doctor_obj['profile'])

        #         name = doctor_obj['name']
        #         name = name.replace('Dr. ', '')

        #         try:
        #             doctor_instance = Doctor.objects.get(name = name, created_at__date__gte=datetime.now() - timedelta(days=2), pmdc_id = doctor_obj['pmdc_id'], heading = doctor_obj['edu_degrees'] if doctor_obj['edu_degrees'] else doctor_obj['specializations'])
        #         except Doctor.MultipleObjectsReturned:
        #             if name not in Udata:
        #                 Udata[name] = 1
        #             else:
        #                 Udata[name] += 1
        #             continue
        #         except Exception as err:
        #             # print(f'{err} :: {name}')
        #             continue
            
        #         print(doctor_instance.name)
        #         # doctor_instance.desc = doctor_obj['profile'] if doctor_obj['profile'] else ''

        #         print(f'{counter}/{len(reader)} Added ::::: ---->>  {name} Saved')
        #         total_users += 1
        #         counter += 1
        #     # print(Udata)
        self.stdout.write(self.style.SUCCESS('Successfully added'))


# name ---> Doctor Name, Username
# doc_gender ---> User Gender Male, Female, female
# doctor_city
# edu_degrees ---> Doctor Heading
# pmdc_id ---> PMDC ID
# profile ---> About/Description
# yearsofexperience ---> 18 ---> Convert to Datetime
# specializations ---> Doctor Speciality
# MainCategory ---> Specialities,Specialities
# MainDiseases ---> Diseases,Diseases
# available_days ---> "M, Tu, W, Th, F, Sa"

# average_wait_time ---> 14

# hospitals 
    # subs_name ---> Hospital Name | Online Video Consultation
    # locality ---> Hospital Location Short Name | Online
    # address ---> Hospital Location Full Address | Speak to doctor through a video call
    # latitude ---> Hospital Location Latitude | null
    # longitude ---> Hospital Location Longitude | null
    # fee
    # city ---> Hospital Location City | Video Consultation
    # available_days ---> "M, Tu, W, Th, F, Sa"

# featured_review ---> Review (Huzaifa)

# services
    # name ---> (Commas seperated Services Name)

# opening_hours ---> "03:00 PM"
