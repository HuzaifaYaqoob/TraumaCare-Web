



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

    def getHospital(self, hospital_object):
        hospital_name = hospital_object['subs_name']

        try:
            hospital = Hospital.objects.get(name = hospital_name)
        except Exception as err:
            admin_user = User.objects.get(mobile_number = '03400193324')
            hospital_profile = Profile.objects.create(
                user = admin_user,
                full_name = hospital_name,
                email = admin_user.email,
                profile_type = 'Hospital',
                is_active = True,
            )
            hospital = Hospital.objects.get(profile = hospital_profile)
            print('Hospital Error : ', str(err))


        locality = hospital_object['locality']
        address = hospital_object['address']
        latitude = hospital_object['latitude']
        longitude = hospital_object['longitude']
        city = hospital_object['city']

        try:
            city = City.objects.get(name__iexact=city)
        except Exception as err:
            city = None
            print('City ERROR : ', str(err))

        location_instance, created = HospitalLocation.objects.get_or_create(
            hospital = hospital,
            name = locality,
        )
        location_instance.country = city.country if city else None
        location_instance.state = city.state if city else None
        location_instance.city = city
        location_instance.street_address = address
        location_instance.lat = latitude
        location_instance.lng = longitude
        location_instance.save()

        
        return [hospital, location_instance]

    def handle(self, *args, **options):
        # with open('https://traumacare.blr1.digitaloceanspaces.com/static/uniqueDoctors.json')
        total_users = User.objects.all().count()
        with open('Files/uniqueDoctors.json' , 'r') as input_file:
            reader = json.load(input_file)
            for doctor_id, doctor_obj in reader.items():
                name = doctor_obj['name']
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
                if doctor_city:
                    try:
                        city_obj = City.objects.get(name__iexact=doctor_city)
                    except Exception as err:
                        print('City ERROR : ', str(err))
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
                doctor_instance.heading = doctor_obj['edu_degrees']
                doctor_instance.pmdc_id = doctor_obj['pmdc_id']
                doctor_instance.desc = doctor_obj['profile']

                for deg in doctor_obj['edu_degrees'].split(','):
                    DoctorEducation.objects.create(
                        doctor = doctor_instance,
                        degree_name = deg.strip(),
                    )

                experience = doctor_obj['yearsofexperience']
                if experience:
                    experience = int(experience)
                    doctor_instance.working_since = f'{2025 - experience}-01-01'

                doctor_instance.save()

                specialities = doctor_obj['MainCategory'].split(',')
                for speciality in specialities:
                    DoctorSpeciality.objects.create(
                        speciality = Speciality.objects.get_or_create(name__iexact=speciality)[0],
                        doctor = doctor_instance,
                    )

                diseases = doctor_obj['MainDiseases'].split(',')
                for disease in diseases:
                    DoctorDiseasesSpeciality.objects.create(
                        disease = Disease.objects.get_or_create(name__iexact=disease)[0],
                        doctor = doctor_instance,
                    )
                
                available_days = doctor_obj['available_days'].split(',')
                for day in available_days:
                    if not day:
                        continue
                    DoctorOnlineAvailability.objects.create(
                        doctor = doctor_instance,
                        day = DAYS_ABBR[day.strip()],
                    )

                opening_hours = doctor_obj['opening_hours'] # 03:00 PM
                opening_time = datetime.strptime(opening_hours, "%I:%M %p")
                end_time = timedelta(hours=3)
                end_time = opening_time + end_time
                opening_time = opening_time.time()

                dynamic_title = 'Morning Slots'
                if opening_time >= datetime.strptime('12:00 PM', "%I:%M %p").time():
                    dynamic_title = 'Afternoon Slots'
                elif opening_time >= datetime.strptime('05:00 PM', "%I:%M %p").time():
                    dynamic_title = 'Evening Slots'
                elif opening_time >= datetime.strptime('08:00 PM', "%I:%M %p").time():
                    dynamic_title = 'Night Slots'


                ola_hospitals = doctor_obj['hospitals']
                for ola_hosp in ola_hospitals:
                    ola_h_name = ola_hosp['subs_name']
                    available_days = ola_hosp['available_days'].split(',')
                    fee = ola_hosp['fee']
                    if fee:
                        fee = int(fee)
                    else:
                        fee = 0

                    if ola_h_name == 'Online Video Consultation':
                        for day in available_days:
                            if not day:
                                continue
                            day = DAYS_ABBR[day.strip()]
                            DoctorTimeSlots.objects.create(
                                doctor = doctor_instance,
                                day = DoctorOnlineAvailability.objects.get(day=day, doctor = doctor_instance),
                                title = dynamic_title,
                                start_time = opening_time,
                                end_time = end_time,
                                fee = fee,
                                service_fee = 25
                            )
                    else:
                        tac_hospital, tac_h_location = self.getHospital(ola_hosp)
                        doc_with_hospital = DoctorWithHospital.objects.create(
                            doctor = doctor_instance,
                            hospital = tac_hospital,
                            location = tac_h_location,
                            phone = 0000,
                        )
                        
                        for day in available_days:
                            if not day:
                                continue
                            day = DAYS_ABBR[day.strip()]
                            DoctorTimeSlots.objects.create(
                                doctor = doctor_instance,
                                doc_hospital = doc_with_hospital,
                                day = DoctorOnlineAvailability.objects.get(day=day, doctor = doctor_instance),
                                title = dynamic_title,
                                start_time = opening_time,
                                end_time = end_time,
                                fee = fee,
                                service_fee = 20,
                                availability_type = 'Hospital'
                            )
                print(f'Added ::::: ---->>  {name} Saved')
                total_users += 1
                break
                pass
            print(len(reader))
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
