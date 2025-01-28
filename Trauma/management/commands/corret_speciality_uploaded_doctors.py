



from django.core.management.base import BaseCommand

from django.conf import settings
from datetime import datetime, timedelta
import time
import re
import random
import json

from Authentication.models import User
from Profile.models import Profile

from Doctor.models import Doctor, DoctorWithHospital, DoctorTimeSlots, DoctorEducation, DoctorDiseasesSpeciality, DoctorSpeciality, DoctorOnlineAvailability
from Hospital.models import Hospital, HospitalLocation
from Trauma.models import Speciality, Disease, City

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
        total_users = User.objects.all().count()
        counter = 0
        Udata = {'available_days' : 0}
        with open('Files/uniqueDoctors.json' , 'r') as input_file:
            reader = json.load(input_file)
            for doctor_id, doctor_obj in reader.items():
                print(doctor_obj['profile'])
                name = doctor_obj['name']
                name = name.replace('Dr. ', '')

                doctor_instance = Doctor.objects.get(name = name)
                # doctor_instance.desc = doctor_obj['profile'] if doctor_obj['profile'] else ''
                continue

                # specialities = doctor_obj.get('MainCategory', '').split(',')
                # print(specialities)
                # for speciality in specialities:
                #     if speciality:
                #         DoctorSpeciality.objects.create(
                #             speciality = Speciality.objects.get_or_create(name=speciality)[0],
                #             doctor = doctor_instance,
                #         )

                # diseases = doctor_obj['MainDiseases'].split(',')
                # for disease in diseases:
                #     DoctorDiseasesSpeciality.objects.create(
                #         disease = Disease.objects.get_or_create(name=disease)[0],
                #         doctor = doctor_instance,
                #     )
                
                print(f'{counter}/{len(reader)} Added ::::: ---->>  {name} Saved')
                total_users += 1
                counter += 1
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
