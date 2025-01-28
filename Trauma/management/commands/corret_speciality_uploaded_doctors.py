



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
                specialities = doctor_obj.get('MainCategory', '')
                if not specialities:
                    print(specialities)
                # if counter <= 5844:
                #     counter += 1
                #     continue
                continue
                # print(json.dumps(doctor_obj))
                # if doctor_obj['available_days'] == '':
                #     print('Skipping', doctor_id)
                #     Udata['available_days'] += 1
                # continue
                name = doctor_obj['name']
                name = name.replace('Dr. ', '')
                doc_gender = doctor_obj['doc_gender']

                username = name.replace(' ', '-').replace('/', '-').replace('--', '-').replace('.', '-').replace('--', '-')
                username = username.lower()
                username = f'{username}-{total_users}'
                email = f'{username}@doctors.traumacare.pk'

                doc_gender = doc_gender.lower().strip().capitalize()
                print(username)

                user = User.objects.create(
                    full_name = name,
                    username = username,
                    email = email,
                    mobile_number = '0000',
                    is_active = True,
                    gender = doc_gender
                )

                doctor_city = doctor_obj['doctor_city']
                if doctor_city == 'Video Consultation':
                    doctor_city = 'Lahore'
                elif doctor_city == 'Peshawar':
                    doctor_city = 'Lahore'
                elif doctor_city == 'Chishtian':
                    doctor_city = 'Chishtian Mandi'


                if doctor_city:
                    try:
                        city_obj = City.objects.get(name__iexact=doctor_city)
                    except Exception as err:
                        print(json.dumps(doctor_obj))
                        print(doctor_city)
                        print('City ERROR Inside : ', str(err))
                    else:
                        user.country = city_obj.country
                        user.state = city_obj.state
                        user.city = city_obj

                user.save()


                doctor_profile = Profile.objects.create(
                    user = user,
                    full_name = user.full_name,
                    email = user.email,
                    profile_type = 'Doctor',
                    is_active = True,
                )

                doctor_instance = Doctor.objects.get(profile = doctor_profile)
                doctor_instance.heading = doctor_obj['edu_degrees'] if doctor_obj['edu_degrees'] else doctor_obj['specializations']
                doctor_instance.pmdc_id = doctor_obj['pmdc_id']
                doctor_instance.desc = doctor_obj['profile'] if doctor_obj['profile'] else ''

                degrees = doctor_obj.get('edu_degrees', '')
                if degrees:
                    for deg in degrees.split(','):
                        DoctorEducation.objects.create(
                            doctor = doctor_instance,
                            degree_name = deg.strip(),
                        )

                experience = doctor_obj['yearsofexperience']
                if experience:
                    experience = int(experience)
                    doctor_instance.working_since = f'{2025 - experience}-01-01'

                doctor_instance.save()

                specialities = doctor_obj.get('MainCategory', '').split(',')
                print(specialities)
                for speciality in specialities:
                    if speciality:
                        DoctorSpeciality.objects.create(
                            speciality = Speciality.objects.get_or_create(name=speciality)[0],
                            doctor = doctor_instance,
                        )

                diseases = doctor_obj['MainDiseases'].split(',')
                for disease in diseases:
                    DoctorDiseasesSpeciality.objects.create(
                        disease = Disease.objects.get_or_create(name=disease)[0],
                        doctor = doctor_instance,
                    )
                
                print(f'{counter}/{len(reader)} Added ::::: ---->>  {name} Saved')
                total_users += 1
                counter += 1
            print(len(reader))
        print(Udata)
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
