from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status

from datetime import datetime, timedelta

from Authentication.models import User



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
                    {'icon' : 'fas fa-user-tie !text-[#F8DB48]', 'title': "Real Users", 'value': real_users.count(), 'desc' : 'Users registered with Real Mobile Numbers'},  ]
    else:
        return Response({'message' : 'Invalid Page',}) 
    
    

    return Response({
        'page' : page,
        'data' : cardData
    }) 
    