from django.shortcuts import render
from django.http import HttpResponseRedirect
from rest_framework.decorators import api_view

from django.contrib import messages

# Create your views here.

from Authentication.models import User

from Trauma.models import Country


def LoginPage(request):
    # return render(request, 'Auth/login.html')
    return render(request, 'Auth/LoginUpdated.html')


def RegisterPage(request):

    countries = Country.objects.filter(
            is_deleted = False,
            is_active = True
        )

    form_countries = []
    for country in countries:
        if country.flag:
            img_html = f'<span><img class="w-5" src="{country.flag.url}" /></span>'
        else:
            img_html = None
        country_html = f'<div class="px-3 py-2 flex items-center justify-between" display-value="SELF" value="{country.id}" data-search="{country.name} {country.dial_code} +{country.dial_code}" ><p>{country.name} (+{country.dial_code})</p>{img_html if img_html is not None else ""}</div>'
        form_countries.append(country_html)

    dial_codes = []
    for country in countries:
        if country.flag:
            img_html = f'<span><img class="w-5" src="{country.flag.url}" /></span>'
        else:
            img_html = None
        country_html = f'<div class="px-3 py-2 flex items-center justify-between" display-value="+{country.dial_code}" value="{country.dial_code}" data-search="{country.name} {country.dial_code} +{country.dial_code}" ><p>{country.name} (+{country.dial_code})</p>{img_html if img_html is not None else ""}</div>'
        dial_codes.append(country_html)

    context = {
        'countries' : form_countries,
        'dial_codes' : dial_codes,
    }


    return render(request, 'Auth/Register.html', context)



def HandleLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        value = username or email

        if not all([value, password]):
            messages.info(request, 'All fields are required')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        query = {}
        if email:
            query['email'] = email
        elif username:
            query['username'] = username

        try:
            user = User.objects.get(
                **query
            )
        except:
            messages.error(request, 'User doesn"t exists')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        

        messages.success(request, 'Login Successfully')
        return HttpResponseRedirect('/auth/login/')
    
    messages.error(request, 'Only POST method allowed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def HandleJoin(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        username = request.POST.get('username', None)
        country_id = request.POST.get('country', None)
        dial_code = request.POST.get('dial_code', None)
        mobile_number = request.POST.get('mobile_number', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)

        if not all([email, username, country_id, dial_code, mobile_number, password, confirm_password]):
            messages.info(request, 'All fields are required')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        try:
            country = Country.objects.get(id = country_id)
        except:
            messages.error(request, 'Country does not exist')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        
        user = User.objects.create_user(
            username = username,
            password = password,
            email = email
        )

        user.dial_code = dial_code
        user.mobile_number = mobile_number
        user.country = country
        user.save()

        messages.success(request, 'User Created Successfully')

        return HttpResponseRedirect('/auth/login/')
    
    messages.error(request, 'Only POST method allowed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

