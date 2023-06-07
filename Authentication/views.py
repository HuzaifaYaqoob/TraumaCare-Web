from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from rest_framework.decorators import api_view


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

# Create your views here.

from Authentication.models import User

from Trauma.models import Country, VerificationCode
from Authentication.Constants.Redirection import NextRedirect, getQueryParams

def LoginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(f'/auth/auto-login-redirection/{getQueryParams(request)}')

    # return render(request, 'Auth/login.html')
    return render(request, 'Auth/LoginUpdated.html')


def OtpVerificationPage(request):
    error_msg1 = 'You are not allowed to access Verification Page'
    
    email = request.GET.get('email', None)

    if not all([email]):
        messages.error(request, error_msg1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    context = {}
    
    try:
        user = User.objects.get(email = email)
        if user.is_email_verified:
            raise Exception(error_msg1)

        codes = VerificationCode.objects.filter(
            user = user, 
            is_expired = False,
            is_deleted = False,
            is_used = False,
        )
        if len(codes) == 0:
            raise Exception(error_msg1)
    except:
        messages.error(request, error_msg1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        context['user'] = user


    # return render(request, 'Auth/login.html')
    return render(request, 'Auth/OTP_verification.html', context)


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



def HandleLogout(request):
    auth.logout(request)
    messages.info(request, 'Logout Successfully')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


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
            
        user = auth.authenticate(username = user.username, password = password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Login Successfully')
            return HttpResponseRedirect(f'/auth/auto-login-redirection/{getQueryParams(request)}')
        else:
            messages.error(request, 'Invalid Credentials')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    messages.error(request, 'Only POST method allowed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def HandleJoin(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        username = request.POST.get('username', None)
        dial_code = request.POST.get('dial_code', None)
        mobile_number = request.POST.get('mobile_number', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirm_password', None)
        
        if not all([email, username, dial_code, mobile_number, password, confirm_password]):
            messages.info(request, 'All fields are required')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        user = User.objects.create_user(
            username = username,
            password = password,
            email = email
        )
        user.dial_code = dial_code
        user.mobile_number = mobile_number
        user.save()

        messages.success(request, 'User Created Successfully')

        # return HttpResponseRedirect('/auth/login/')
        return HttpResponseRedirect(f'/auth/verification/otp/?email={user.email}')
    
    messages.error(request, 'Only POST method allowed')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def handleOtp(request):
    email = request.GET.get('email', None)
    code = request.POST.get('code', None)

    if not all([email, code]):
        messages.info(request, 'Invalid Email or Code!')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    try:
        user = User.objects.get(email = email)
    except:
        messages.error(request, 'Invalid User')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        try:
            code = VerificationCode.objects.get(
                user = user, 
                is_expired = False,
                is_deleted = False,
                is_used = False,
                code = code
            )
        except:
            messages.error(request, 'Invalid Code')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        user.is_email_verified = True
        user.is_active = True
        user.save()
        code.delete()
        messages.success(request, 'Account Verified!')
        return HttpResponseRedirect('/auth/login/')
    

def AutoLoginRedirection(request):
    next_url = NextRedirect(request)
    if next_url:
        return HttpResponseRedirect(next_url)
    
    return HttpResponseRedirect('/')
    


@login_required(login_url='/auth/login/')
def CreateNewBusinessProfileRedirection(request):
    user = request.user
    auth_token = user.auth_token

    url = f'{settings.ACCOUNT_TRAUMACARE_URL}/auth/auto_authentication/?user_id={user.id}&auth_token={auth_token}&redirection_source=tc-rex-doc-uri&business_profile=Doctor'
    # redirection_source=tc-rex-doc-uri

    return HttpResponseRedirect(url)
    
    