from django.shortcuts import render

# Create your views here.


from Trauma.models import Country


def LoginPage(request):
    # return render(request, 'Auth/login.html')
    return render(request, 'Auth/LoginUpdated.html')


def RegisterPage(request):
    context = {
        'countries' : Country.objects.filter(
            is_deleted = False,
            is_active = True
        )
    }
    return render(request, 'Auth/Register.html', context)