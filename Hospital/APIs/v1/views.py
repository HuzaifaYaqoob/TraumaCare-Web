

from rest_framework import status, response
Response = response.Response



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

{
    "active_step": 4,
    "email": "admin@gmail.com",
    "full_name": "Huzaifa Yaqoob",
    "mobile_number": "92-3026431525",
    "user_type": "Hospital",
    "healthcare_facility_type": "Pharmacy",
    "healthcare_facility_name": "Azeem Pharmacy",
    "locations": [
        {
            "address_name": "Johar Town Lahore Branch",
            "address": "Johar Town",
            "contactDetails": [
                {
                    "contact_type": "EMAIL",
                    "contact_title": "Emergency",
                    "email": "redexpo.officialmail@gmail.com"
                }
            ]
        }
    ],
    "media": {
        "profile_image": {},
        "id_card_front": {},
        "id_card_back": {},
        "license_file": {}
    }
}