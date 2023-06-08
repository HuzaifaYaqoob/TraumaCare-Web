

from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from Doctor.models import Doctor, DoctorSpeciality, DoctorDiseasesSpeciality, DoctorOnlineAvailability, DoctorTimeSlots, Doctor24By7, DoctorMedia
from Profile.models import Profile
from Trauma.models import Speciality, Disease


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createDoctorProfile(request):
    user_type = request.data.get('user_type', None)
    email = request.data.get('email', None)
    full_name = request.data.get('full_name', None)
    heading = request.data.get('heading', None)
    mobile_number = request.data.get('mobile_number', None)
    working_since = request.data.get('working_since', None)
    
    specialities = request.data.getlist('specialities', None)
    diseases = request.data.getlist('diseases', None)

    # doctor_fee = request.data.get('doctor_fee', None)

    # slots = request.data.get('slots', None)
    # availability_type = request.data.get('availability', None)
    profile_image = request.data.get('profile_image', None)
    id_card_front = request.data.get('id_card_front', None)
    id_card_back = request.data.get('id_card_back', None)
    license_file = request.data.get('license_file', None)


    required_fields = [
        user_type,
        email,
        full_name,
        heading,
        mobile_number,
        working_since,
        specialities,
        diseases,
        # availability_type,
        profile_image,
        id_card_front,
        id_card_back,
        license_file,
    ]

    # if availability_type == '24_HOURS_OPEN':
    #     required_fields.append(doctor_fee)
    # elif availability_type == 'AVAILABILITY_TIME_SLOTS':
    #     required_fields.append(slots)

    if not all(required_fields):
        return Response({
            'status' : False,
            'status_code' : 400,
            'response' : {
                'message' : 'Missing required fields.',
                'data' : {},
                'fields' : [
                    'user_type' ,
                    'email' ,
                    'full_name' ,
                    'heading' ,
                    'mobile_number' ,
                    'working_since' ,
                    'specialities' ,
                    'diseases' ,
                    # 'slots' ,
                    # 'doctor_fee' ,
                    # 'availability' ,
                    'profile_image',
                    'id_card_front',
                    'id_card_back',
                    'license_file',
                ]
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    user_type = user_type.lower()
    if user_type != 'doctor':
        return Response({
            'status' : False,
            'status_code' : 400,
            'response' : {
                'message' : 'Only doctor profile can be created.',
                'data' : {}
            }
        }, status=status.HTTP_400_BAD_REQUEST)
    
    doctor_profile, is_created = Profile.objects.get_or_create(
        user = request.user,
        profile_type = 'Doctor'
    )

    dial_code, m_number = mobile_number.split('-')
    dial_code = dial_code.replace('+', '')

    doctor = Doctor.objects.create(
        user = request.user,
        profile = doctor_profile,
        email = email,
        name = full_name,
        heading = heading,
        dial_code = dial_code,
        mobile_number = m_number,
        working_since = working_since,
        # online_availability = availability_type,
    )

    specialities = [DoctorSpeciality(doctor = doctor, speciality = Speciality.objects.get(id = speciality)) for speciality in specialities]
    DoctorSpeciality.objects.bulk_create(specialities)

    diseases = [DoctorDiseasesSpeciality(doctor = doctor, disease = Disease.objects.get(id = disease)) for disease in diseases]
    DoctorDiseasesSpeciality.objects.bulk_create(diseases)

    
    # if availability_type == '24_HOURS_OPEN':
    #     Doctor24By7.objects.create(
    #         doctor = doctor,
    #         fee = doctor_fee['doctor_fee'],
    #         discount = doctor_fee['discount'],
    #         service_fee = doctor_fee['our_service_fee'],
    #     )

    # elif availability_type == 'AVAILABILITY_TIME_SLOTS':
    #     for day, timeslots in slots.items():
    #         doctor_day = DoctorOnlineAvailability.objects.create(
    #             doctor = doctor,
    #             day = day,
    #         )
    #         created_slots = []
    #         for tm_slot in timeslots:
    #             created_slots.append(DoctorTimeSlots(
    #                 doctor = doctor,
    #                 day = doctor_day,
    #                 start_time = tm_slot['start_time'],
    #                 end_time = tm_slot['end_time'],
    #                 fee = tm_slot['doctor_fee'],
    #                 discount = tm_slot['discount'],
    #                 service_fee = tm_slot['our_service_fee'],
    #             ))
    #         DoctorTimeSlots.objects.bulk_create(created_slots)
    
    medias = [
        [profile_image, 'Profile Image'],
        [id_card_front, 'CNIC Front'],
        [id_card_back, 'CNIC Back'],
        [license_file, 'License'],
    ]

    medias = [DoctorMedia(doctor = doctor, file = med[0], file_type = med[1]) for med in medias]
    DoctorMedia.objects.bulk_create(medias)
    

    return Response({
        'status' : True,
        'status_code' : 200,
        'response' : {
            'message' : 'Doctor Profile created Successfully.',
            'data' : {}
        }
    }, status=status.HTTP_201_CREATED)


# {
#     "active_step": 5,
#     "user_type": "Doctor",
#     "email": "huzaifa.officialmail@gmail.com",
#     "full_name": "Huzi Chuzi",
#     "heading": "MBBS PHD in Medicine & Surgery, Ent Specialist are Surgeons ",
#     "mobile_number": "+92-3187834096",
#     "working_since": "2023-04-12",
#     "specialities": [
#         "7624be1b-817f-4930-80ef-2ff7e9654965",
#         "3fca1fed-752b-48c3-ab3b-55ad30e887cf",
#         "f0677399-2a2e-47fe-90b9-5ebf409f897b",
#         "fafe6ecd-2fd2-4f83-9907-7c112cbbba67",
#         "65c1d71b-3651-43aa-808a-7f926f312eed",
#         "172afda2-7c47-46e0-a4ea-642dab4fb2ae",
#         "bd2cbb3b-854e-466c-a9d8-99eaf971aa3d",
#         "f6c5499e-d7df-4a63-ad85-39cd56844244"
#     ],
#     "diseases": [
#         "4998838c-35a1-4d6e-b06f-b1ccd8f3339a",
#         "acc7977b-b74e-45cd-90c3-8c5519a211f8",
#         "d5a4f57c-5b33-42ff-8880-6d89c07c200d",
#         "3c3c3b82-ae28-4b22-819b-a43d398cd06a",
#         "cf1e4d04-682c-4a51-b3a8-d13d00033840",
#         "07df51ee-e987-485e-89c4-781497f9abc2",
#         "b179bd2c-cf96-4798-bb39-cb5e0f16da27",
#         "cc7b6723-6069-46a5-87fa-99c59c0fba8a",
#         "63bf9fa4-836a-412c-ad57-1a673001d06a",
#         "c8dbcd7e-63f4-4aa9-9792-cab3c3c8ee46"
#     ],
#     "slots": {
#         "Wednesday": [
#             {
#                 "start_time": "00:00:00",
#                 "end_time": "02:00:00",
#                 "doctor_fee": "3000",
#                 "discount": "10",
#                 "our_service_fee": 7,
#                 "total": "2910.00",
#                 "start_label": "12:00 AM",
#                 "duration": 120,
#                 "end_label": "02:00 AM",
#                 "day": "Wednesday"
#             }
#         ],
#         "Thursday": [
#             {
#                 "start_time": "08:40:00",
#                 "end_time": "09:00:00",
#                 "doctor_fee": "4000",
#                 "discount": 0,
#                 "our_service_fee": 7,
#                 "total": "4280.00",
#                 "start_label": "08:40 AM",
#                 "duration": 20,
#                 "end_label": "09:00 AM",
#                 "day": "Thursday"
#             },
#             {
#                 "start_time": "11:00:00",
#                 "end_time": "17:40:00",
#                 "doctor_fee": "2000",
#                 "discount": 0,
#                 "our_service_fee": 7,
#                 "total": "2140.00",
#                 "start_label": "11:00 AM",
#                 "duration": -320,
#                 "end_label": "05:40 PM",
#                 "day": "Thursday"
#             }
#         ],
#         "Friday": [
#             {
#                 "start_time": "10:00:00",
#                 "end_time": "17:40:00",
#                 "doctor_fee": "3000",
#                 "discount": 0,
#                 "our_service_fee": 7,
#                 "total": "3210.00",
#                 "start_label": "10:00 AM",
#                 "duration": -260,
#                 "end_label": "05:40 PM",
#                 "day": "Friday"
#             },
#             {
#                 "start_time": "18:40:00",
#                 "end_time": "23:40:00",
#                 "doctor_fee": "3000",
#                 "discount": "6",
#                 "our_service_fee": 7,
#                 "total": "3030.00",
#                 "start_label": "06:40 PM",
#                 "duration": 300,
#                 "end_label": "11:40 PM",
#                 "day": "Friday"
#             }
#         ]
#     },
#     "availability": "AVAILABILITY_TIME_SLOTS",
#     "media": {
#         "profile_image": {
#             "file": {}
#         },
#         "id_card_front": {
#             "file": {}
#         },
#         "id_card_back": {
#             "file": {}
#         },
#         "license_file": {
#             "file": {}
#         }
#     }
# }