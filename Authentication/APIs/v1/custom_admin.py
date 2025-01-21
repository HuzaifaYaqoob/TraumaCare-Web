from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from datetime import datetime, timedelta

from Authentication.models import User
from Doctor.models import DoctorRequest
from Hospital.models import HospitalRequest



@api_view(['GET'])
@permission_classes([AllowAny])
def getAdminTopTiles(request):
    current_page = request.GET.get('current_page', None)
    if not current_page:
        return Response({'message' : 'Invalid Page',}) 
    
    pages = []
    for i in current_page.split('/'):
        if i:
            pages.append(i)
    page = '.'.join(pages)

    today = datetime.now()
    prev_svn_days = today - timedelta(days=7)
    range_date = (prev_svn_days.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d'))
    if page == 'admin.Authentication.user':
        users = User.objects.filter(is_deleted=False)
        active_users = users.filter(is_active=True)
        new_users = users.filter(joined_at__date__range = range_date)
        real_users = users.exclude(mobile_number='0000').distinct()
        cardData = [{'icon' : 'fas fa-th-large !text-[#0755E9]', 'title': "Total users", 'value': users.count(), 'desc' : 'Total Users Registered on this platform'}, 
                    {'icon' : 'fa fa-plus-circle !text-[#F01275]', 'title': "New Users", 'value': new_users.count(), 'desc' : 'News Users in past 7 days'},
                    {'icon' : 'fas fa-user !text-[#05DC75]', 'title': "Active Users", 'value': active_users.count(), 'desc' : 'User with status Active'}, 
                    {'icon' : 'fas fa-user-tie !text-[#F8DB48]', 'title': "Real Users", 'value': real_users.count(), 'desc' : 'Users registered with Real Mobile Numbers'},  
                ]
    elif page == 'admin.Administration.phonemessage':
        from Administration.models import PhoneMessage
        msgs = PhoneMessage.objects.filter(created_at__date = today)
        cardData = [
            {'icon' : 'fa fa-plus-circle !text-[#F01275]', 'title': "Todays SMS", 'value': msgs.count(), 'desc' : 'Todays Messages'},
        ]
    elif page == 'admin':
        users = User.objects.filter(is_deleted=False)
        new_users = users.filter(joined_at__date__range = range_date)

        doctors_requests = DoctorRequest.objects.filter(is_active=True)
        pending_requests = doctors_requests.filter(is_onboarded=False)

        hospital_requests = HospitalRequest.objects.filter(is_active=True)
        h_pending_requests = hospital_requests.filter(is_onboarded=False)
        cardData = [
            {'icon' : 'fa fa-plus-circle !text-[#F01275]', 'title': "New Users", 'value': new_users.count(), 'desc' : 'News Users in past 7 days'},
            # Doctors Request for those doctors who submitted onboarding form & our team will call them for verification & onboarding & registering them into our system
            {'icon' : 'fa fa-user-tie !text-[#F8DB48]', 'title': "Doctors Requests", 'value': f'{doctors_requests.count()}/{pending_requests.count()}', 'desc' : 'Solved/Unsolved Request to join our platform'},
            {'icon' : 'fa fa-user-tie !text-[#05DC75]', 'title': "Hospitals Requests", 'value': f'{hospital_requests.count()}/{h_pending_requests.count()}', 'desc' : 'Solved/Unsolved Request to join our platform'},
        ]
    else:
        return Response({'message' : 'Invalid Page',}) 
    
    

    return Response({
        'page' : page,
        'data' : cardData
    }) 
    