



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

        if city == 'Video Consultation':
            city = 'Lahore'
        elif city == 'Peshawar':
            city = 'Lahore'
        elif city == 'Chishtian':
            city = 'Chishtian Mandi'

        try:
            city = City.objects.get(name__iexact=city)
        except Exception as err:
            print(city)
            city = None
            print('City ERROR Outside : ', str(err))

        location_instance, created = HospitalLocation.objects.get_or_create(
            hospital = hospital,
            name = locality,
        )
        location_instance.country = city.country if city else None
        location_instance.state = city.state if city else None
        location_instance.city = city
        location_instance.street_address = address
        location_instance.lat = latitude if latitude else ''
        location_instance.lng = longitude if longitude else ''
        location_instance.save()

        
        return [hospital, location_instance]

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
                
                available_days = doctor_obj['available_days'].split(',')
                for day in available_days:
                    if not day:
                        continue
                    DoctorOnlineAvailability.objects.create(
                        doctor = doctor_instance,
                        day = DAYS_ABBR[day.strip()],
                    )

                opening_hours = doctor_obj.get('opening_hours', '03:00 PM') # 03:00 PM
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

                    print(ola_h_name)
                    if ola_h_name == 'Online Video Consultation' or 'Video Consultation' == ola_hosp['city']:
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
                            phone = '0000',
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
