

from django.shortcuts import render, redirect

from Authentication.models import Role

def OrganizationHierarchyPage(request):
    context = {}

    ceo = Role.objects.get(rank='1')
    context['TC_CEO'] = ceo
    return render(request, 'CustomAdminTemplates/organization_admin.html', context)