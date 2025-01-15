

from django.shortcuts import render, redirect, reverse

from Authentication.models import Role

from Pharmaceutical.models import Pharmaceutical
from Product.models import Product


def SuperUserDashboard(request):
    context = {}
    return render(request, 'CustomAdminTemplates/superuser_dashboard.html', context)

def AdminTestPage(request):
    context = {}

    if request.method == 'POST':
        first = request.POST.get('first')
        second = request.POST.get('second')

        first = Pharmaceutical.objects.get(id=first)
        second = Pharmaceutical.objects.get(id=second)

        first_products = Product.objects.filter(manufacturer = first)
        first_products.update(manufacturer = second)

        return redirect(reverse('AdminTestPage'))


    context['first'] = Pharmaceutical.objects.all().order_by('name')
    context['second'] = Pharmaceutical.objects.all().order_by('name')
    return render(request, 'CustomAdminTemplates/test.html', context)

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