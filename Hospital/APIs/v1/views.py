

import json
from rest_framework import status, response, decorators, permissions
Response = response.Response

from Hospital.models import Hospital, HospitalLocation, HospitalMedia, LocationContact
from Profile.models import Profile




@decorators.api_view(['POST'])
@decorators.permission_classes([permissions.IsAuthenticated])
def createHospitalProfile(request):
    user_type = request.data.get('user_type', None)
    healthcare_facility_type = request.data.get('healthcare_facility_type', None)
    healthcare_facility_name = request.data.get('healthcare_facility_name', None)
    locations = request.data.get('locations', None)

    profile_image = request.data.get('profile_image', None)
    id_card_front = request.data.get('id_card_front', None)
    id_card_back = request.data.get('id_card_back', None)
    license_file = request.data.get('license_file', None)

    required_fields = [
        user_type,
        healthcare_facility_type,
        healthcare_facility_name,
        locations,
        profile_image,
        id_card_front,
        id_card_back,
        license_file,
    ]

    if not all(required_fields):
        return Response({
            'status' : False,
            'status_code' : 400,
            'response' : {
                'message' : 'Missing required fields.',
                'data' : {},
                'fields' : [
                    'user_type',
                    'healthcare_facility_type',
                    'healthcare_facility_name',
                    'locations',
                    'profile_image',
                    'id_card_front',
                    'id_card_back',
                    'license_file',
                ]
            }
        }, status=status.HTTP_400_BAD_REQUEST)

    hospital_profile, is_created = Profile.objects.get_or_create(
        user = request.user,
        profile_type = healthcare_facility_type
    )

    hospitalInstance = Hospital.objects.create(
        user = request.user,
        profile = hospital_profile,
        facility_type = user_type,
        name = healthcare_facility_type,
    )

    if locations:
        locations = json.loads(locations)
        for hospital_location in locations:
            address_name = hospital_location.get('address_name', None)
            address = hospital_location.get('address', None)
            contactDetails = hospital_location.get('contactDetails', None)

            locationInstance = HospitalLocation.objects.create(
                user = request.user,
                profile = hospital_profile,
                hospital = hospitalInstance,
                name = address_name,
                street_address = address,
            )

            for contact in contactDetails:
                contact_type = contact.get('contact_type', None)
                contact_title = contact.get('contact_title', None)

                contactInstance = LocationContact(
                    user = request.user,
                    profile = hospital_profile,
                    hospital = hospitalInstance,
                    location = locationInstance,
                    contact_type = contact_type,
                    contact_title = contact_title,
                )
                if contact_type == 'EMAIL' :
                    email = contact.get('email', None)
                    contactInstance.email = email
                else:
                    phone_number = contact.get('phone_number', None)
                    if phone_number:
                        user_dc, user_pn = phone_number.split('-')
                        contactInstance.dial_code = user_dc
                        contactInstance.mobile_number = user_pn
                
                contactInstance.save()

    return Response({
        'status' : True,
        'status_code' : 201,
        'response' : {
            'message' : f'{healthcare_facility_type} profile created successfully.',
            'data' : {},
        }
    }, status=status.HTTP_201_CREATED)



# {
#     "active_step": 4,
#     "email": "admin@gmail.com",
#     "full_name": "Huzaifa Yaqoob",
#     "mobile_number": "92-3026431525",
#     "user_type": "Hospital",
#     "healthcare_facility_type": "Pharmacy",
#     "healthcare_facility_name": "Azeem Pharmacy",
#     "locations": [
#         {
#             "address_name": "Johar Town Lahore Branch",
#             "address": "Johar Town",
#             "contactDetails": [
#                 {
#                     "contact_type": "EMAIL",
#                     "contact_title": "Emergency",
#                     "email": "redexpo.officialmail@gmail.com"
#                 }
#             ]
#         }
#     ],
#     "media": {
#         "profile_image": {},
#         "id_card_front": {},
#         "id_card_back": {},
#         "license_file": {}
#     }
# }