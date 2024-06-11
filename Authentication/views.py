from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token


from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from Constants.Emails.OtpEmail import sendOtpEmail

# Create your views here.

from Authentication.models import User

from Trauma.models import Country, VerificationCode
from Authentication.Constants.Redirection import NextRedirect, getQueryParams
from ChatXpo.models import XpoChat

def LoginPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(f'/auth/auto-login-redirection/{getQueryParams(request)}')

    # return render(request, 'Auth/login.html')
    return render(request, 'Auth/LoginUpdated.html')


def ResetPasswordPage(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(f'/')

    email = request.GET.get('email', None)
    purpose = request.GET.get('purpose', None)

    error_msg1 = 'You are not allowed to access reset password page'
    if not all([email, purpose]):
        messages.error(request, error_msg1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    try:
        user = User.objects.get(
            email = email,
            is_active = True,
            is_blocked = False,
            is_deleted = False,
        )
    except:
        messages.error(request, error_msg1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        codes = VerificationCode.objects.filter(
            user = user,
            otp_type = 'FORGOT_PASSWORD'
        )
        if len(codes) == 0:
            messages.error(request, error_msg1)
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        

        return render(request, 'Auth/ResetPasswordPage.html')


def OtpVerificationPage(request):
    error_msg1 = 'You are not allowed to access Verification Page'
    
    email = request.GET.get('email', None)
    

    if not all([email]):
        messages.error(request, error_msg1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    context = {}
    
    purpose = request.GET.get('purpose', 'EMAIL_VERIFICATION')
    try:
        user = User.objects.get(email = email)
        if user.is_email_verified and purpose == 'EMAIL_VERIFICATION':
            raise Exception(error_msg1)
    
        queries = {}
        if purpose == 'FORGOT_PASSWORD':
            queries['otp_type'] = 'FORGOT_PASSWORD'

        codes = VerificationCode.objects.filter(
            user = user, 
            is_expired = False,
            is_deleted = False,
            is_used = False,
            **queries
        )
        if len(codes) == 0:
            raise Exception(error_msg1)
    except:
        messages.error(request, error_msg1)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        resend = request.GET.get('resend', None)
        if resend is not None:
            codes.delete()
            otp = VerificationCode.objects.create(
                user = user
            )
            sendOtpEmail(
                {
                    'user' : user,
                    'verification_code' : otp
                }
            )
            messages.success(request, 'OTP resent to your Email')
            return HttpResponseRedirect(f'/auth/verification/otp/?email={user.email}')
        
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

def ForgotPasswordPage(request):
    return render(request, 'Auth/ForgotPasswordPage.html')


def HandleLogout(request):
    chat_id = request.session.get('chat_id', None)
    auth.logout(request)

    if chat_id:
        try:
            chat = XpoChat.objects.get(uuid = chat_id)
        except:
            del request.session['chat_id']
        else:
            request.session['chat_id'] = chat_id
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
            chat_id = request.session.get('chat_id', None)
            if chat_id:
                try:
                    user_chat = XpoChat.objects.get(uuid = chat_id)
                except:
                    request.session['chat_id'] = None
                else:
                    user_chat.user = user
                    user_chat.save()

            messages.success(request, 'Login Successfully')
            response = HttpResponseRedirect(f'/auth/auto-login-redirection/{getQueryParams(request)}')
            
            user_token, created = Token.objects.get_or_create(user = user)
            response.set_cookie('auth_token', user_token.key)
            response.set_cookie('user_id', f'{user.id}')
            return response
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


def ForgotPasswordHandler(request):
    if request.method != 'POST':
        messages.error(request, 'Only POST method allowed')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    email = request.POST.get('email', None)
    if not all([email]):
        messages.info(request, 'All fields are required')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    try:
        user = User.objects.get(
            email = email,
            is_active = True,
            is_blocked = False,
            is_deleted = False,
        )
    except:
        messages.error(request, 'User does not exist with this email.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        codes = VerificationCode.objects.filter(
            user = user, 
            is_expired = False,
            is_deleted = False,
            is_used = False,
        )
        codes.delete()
        otp = VerificationCode.objects.create(
            user = user,
            otp_type = 'FORGOT_PASSWORD'
        )
        sendOtpEmail(
            {
                'user' : user,
                'verification_code' : otp
            }
        )
        messages.success(request, 'OTP sent to your Email')
        return HttpResponseRedirect(f'/auth/verification/otp/?email={user.email}&purpose=FORGOT_PASSWORD&next=/auth/reset-password/')

def ChangePasswordHandler(request):
    if request.method != 'POST':
        messages.error(request, 'Only POST method allowed')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    email = request.GET.get('email', None)
    purpose = request.GET.get('purpose', None)
    password = request.POST.get('password', None)

    if not all([email, purpose, password]):
        messages.info(request, 'All fields are required')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
    try:
        user = User.objects.get(
            email = email,
            is_active = True,
            is_blocked = False,
            is_deleted = False,
        )
    except:
        messages.error(request, 'User does not exist with this email.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        user.set_password(password)
        user.save()
        codes = VerificationCode.objects.filter(
            user = user, 
        )
        codes.delete()
        messages.success(request, 'Password Changed Successfully')
        next_url = request.GET.get('next', None)
        return HttpResponseRedirect(next_url if next_url else f'/auth/login/')


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
        purpose = request.GET.get('purpose', None)
        try:
            code = VerificationCode.objects.get(
                user = user, 
                is_expired = False,
                is_deleted = False,
                is_used = False,
                code = code
            )
        except Exception as err:
            messages.error(request, err if err else 'Invalid Code')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        user.is_email_verified = True
        user.is_active = True
        user.save()
        if purpose == 'FORGOT_PASSWORD':
            code.is_expired = True
            code.is_used = True
            code.save()
        else:
            code.delete()
        messages.success(request, 'Email Verified!')
        getQueries = '?'
        next_url = request.GET.get('next', None)
        for param, val in request.GET.items():
            if param == 'next' and purpose == 'FORGOT_PASSWORD':
                pass
            else:
                getQueries += f'{param}={val}&'
            
        return HttpResponseRedirect(f'{next_url}{getQueries}next=/auth/login/' if next_url else f'/auth/login/{getQueries}')
    

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
    
    