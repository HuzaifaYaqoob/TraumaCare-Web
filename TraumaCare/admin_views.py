

from django.shortcuts import render, redirect, reverse

from Authentication.models import Role

def SuperUserDashboard(request):
    context = {}
    return render(request, 'CustomAdminTemplates/superuser_dashboard.html', context)

def OrganizationHierarchyPage(request):
    selected_role = request.GET.get('selected_role', None)
    context = {}

    try:
        FirstRole = Role.objects.get(id=selected_role)
    except:
        FirstRole = Role.objects.get(rank='1')

    breadcrumbs = [
        # {'name' : 'Home', 'url' : ''},
        
    ]
    finished = False
    currentRole = FirstRole

    while not finished:
        if currentRole.parent:
            breadcrumbs.insert(0, {'name' : currentRole.parent.name, 'url' : f"{reverse('OrganizationHierarchyPage')}?selected_role={currentRole.parent.id}"})
            currentRole = currentRole.parent
        else:
            finished = True
        
    breadcrumbs.insert(0, {'name' : 'Dashboard', 'url' : '/admin/'})
    breadcrumbs.append({'name' : FirstRole.name, 'url' : f"#"})
    context['FirstRole'] = FirstRole
    context['breadcrumbs'] = breadcrumbs
    return render(request, 'CustomAdminTemplates/organization_admin.html', context)