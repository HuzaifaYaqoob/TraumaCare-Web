

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

from Doctor.models import Doctor, DoctorMedia, DoctorRequest
from Trauma.models import Speciality, Disease, State, Country, City, ShortLink
from django.db.models import Case, When, Min, Sum, Q, Count, Prefetch, F, Value, Subquery, OuterRef
from rest_framework.authtoken.models import Token
from Secure.models import ApplicationReview
from Blog.models import BlogPost, BlogMedia
from django.contrib.postgres.search import SearchHeadline, SearchQuery

from Hospital.models import Hospital, HospitalLocation, LocationContact, HospitalMedia, HospitalRequest

from Profile.models import Profile
from Administration.models import PageAnalytics

from datetime import datetime
from Product.models import Product, ProductStock

# from django.views.decorators.cache import cache_page

def Custom500ErrorPage(request):
    return render(request, '500.html')

def Custom400ErrorPage(request, exception):
    return render(request, '500.html')

def shortCodeRedirect(request, short_code_id):
    try:
        link = ShortLink.objects.get(id = short_code_id)
    except:
        return redirect('homePage')
    else:
        return redirect(link.long_link)


# @cache_page(60 * 15)
def homePage(request):
    context = {}

    doctors = Doctor.objects.filter(
        is_active = True,
        is_deleted = False,
        is_blocked = False,
    ).prefetch_related(
        'doctor_medias',
        'doctor_reviews',
        'doctor_available_days',
    ).order_by('?')

    context['doctors'] = doctors[:8]
    context['blog_posts'] = BlogPost.objects.annotate(
            media = Count('blog_post_medias')
        ).filter(
            media__gt = 0
        ).select_related('category',).prefetch_related('blog_post_medias').order_by('-created_at')[:4]
        
    context['application_reviews'] = ApplicationReview.objects.filter(is_deleted = False, is_blocked=False).order_by('-rating')[0:20]


    other_medicines = Product.objects.filter(
        is_active=True,
        is_deleted=False,
        is_blocked=False
    ).select_related('store').prefetch_related(
        'product_images',
        'product_stocks',
        'product_stocks__location',
    ).order_by('?')[:10]

    context['medicines'] = other_medicines


    return render(request, 'Home/index.html', context)



def onboarding(request):

    onboarding_type = request.GET.get('onboarding_type',  None)
    if onboarding_type == None:
        return redirect('/onboarding/?onboarding_type=doctor')
    
    if request.method == 'POST':
        page_analytic = PageAnalytics.objects.create(
            urls = f'Post Request',
            value = 1,
            analytic_type = 'Visits'
        )
        if onboarding_type == 'doctor':
            page_analytic.urls = page_analytic.urls + ' --- Doctor Submitted'
            page_analytic.save()

            full_name = request.POST.get('full_name', None)
            gender = request.POST.get('gender', None)
            speciality = request.POST.get('speciality', None)
            phone = request.POST.get('phone', None)

            DoctorRequest.objects.create(
                name = full_name,
                phone = phone,
                speciality = speciality,
                gender = gender,
            )
            page_analytic.urls = page_analytic.urls + ' --- Saved'
            page_analytic.save()
            messages.success(request, 'Thanks for submitting your application! Our team will get back to you soon.')
            page_analytic.urls = page_analytic.urls + ' --- Message & Next Return'
            page_analytic.save()
            return redirect('/')
            
        else:
            hospital_name = request.POST.get('hospital_name', None)
            phone = request.POST.get('phone', None)

            HospitalRequest.objects.create(
                name = hospital_name,
                phone = phone,
            )
            messages.success(request, 'Thanks for submitting your application! Our team will get back to you soon.')
            return redirect('/')
    
    context = {
        'remove_footer' : True,
        'hideChatWidget' : True,
    }
    page_analytic = PageAnalytics.objects.create(
        urls = request.get_full_path(),
        value = 1,
        analytic_type = 'Visits'
    )
    if onboarding_type == 'doctor':
        new_page_id = PageAnalytics.objects.create(
            urls = f'Doctor --- page_analytic id :: {str(page_analytic.id)}',
            value = 1,
            analytic_type = 'Visits'
        )
        # if request.user.has_doctor_profile:
        #     messages.info(request, 'Doctor Profile Already Exists!')
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        context['page_analytics_id'] = new_page_id.id
        return render(request, 'DoctorOnboarding.html', context)
    elif onboarding_type == 'hospital':
        # if request.user.has_hospital_profile:
        #     messages.info(request, 'Hospital Profile Already Exists!')
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        # context['states'] = State.objects.filter(is_deleted = False, is_active = True, country__name__icontains = 'pakistan').order_by('name')
        # context['cities'] = City.objects.filter(is_deleted = False, is_active = True, country__name__icontains = 'pakistan').order_by('name')
        return render(request, 'HospitalOnboarding.html', context)
    else:
        return redirect('/onboarding/?onboarding_type=doctor')

def chatXpo_redirection(request):
    if not request.user.is_authenticated:
        return redirect('/auth/login?next=/chatxpo', )

    user_id = request.user.id
    token, created = Token.objects.get_or_create(user = request.user)
    auth_token = token

    accounts_url = f'{settings.ACCOUNT_TRAUMACARE_URL}/auto_login?user_id={user_id}&auth_token={auth_token}'
    reponse = redirect(accounts_url)
    return reponse

def email_view(request):
    path = request.GET.get('path')
    return render(request, path)


def FeedPage(request):
    return render(request, 'Feed/feedPage.html')

def SpecialitiesPage(request):
    return render(request, 'Speciality/specialities.html')

def SingleSpecialityPage(request, speciality_slug):
    
    try:
        speciality = Speciality.objects.get(
            slug = speciality_slug,
            is_deleted = False,
            is_active = True,
        )
    except:
        messages.error(request, 'Invalid Speciality URL!')
        messages.info(request, 'Explore more here!')
        return redirect('SpecialitiesPage')
    else:
        doctor_uri = request.GET.get('doctor_uri', None)
    
        doctors_order_by = []
        if doctor_uri:
            doctors_order_by.append((Case(When(id=doctor_uri, then=0), default=1)))

        context = {}
        context['speciality'] = speciality
        context['doctors'] = Doctor.objects.filter(
            is_active = True,
            is_deleted = False,
            is_blocked = False,
        ).order_by(*doctors_order_by)
        return render(request, 'Speciality/speciality.html', context)


# Diseases Handler 

def DiseasesViewAllPage(request):
    return render(request, 'Disease/Diseases.html')

def SingleDiseasePage(request, disease_slug):
    try:
        disease = Disease.objects.get(
            slug = disease_slug,
            is_deleted = False,
            is_active = True,
        )
    except:
        messages.error(request, 'Invalid disease URL!')
        messages.info(request, 'Explore more here!')
        return redirect('DiseasesViewAllPage')
    else:
        context = {}
        context['disease'] = disease
    return render(request, 'Disease/SingleDiseaseView.html', context)

def test(request):
    return render(request, 'prescription.html')

def CartPage(request):
    return render(request, 'User/cart.html')

def searchFilterPage(request):
    # return render(request, 'Search/booklabtest.html')
    searchText = request.GET.get('query', '')

    available_today = request.GET.get('available_today', None)
    video_consultaion = request.GET.get('video_consultaion', None)
    discounts = request.GET.get('discounts', None)
    doctor_gender = request.GET.get('doctor_gender', None)
    most_experienced = request.GET.get('most_experienced', None)
    lowest_fee = request.GET.get('lowest_fee', None)
    highest_rating = request.GET.get('highest_rating', None)
    most_reviews = request.GET.get('most_reviews', None)
    disease_slugs = request.GET.getlist('disease', None)
    speciality_slugs = request.GET.getlist('speciality', None)
    hospital_slugs = request.GET.getlist('hospital', None)

    query = {
    }

    annotate_query = {}
    order_query = []
    reverse = False

    

    if '' in disease_slugs:
        disease_slugs.remove('')
    if len(disease_slugs) > 0:
        query['doctor_disease_specialities__disease__slug__in'] = disease_slugs

    if '' in speciality_slugs:
        speciality_slugs.remove('')
    if len(speciality_slugs) > 0:
        query['doctor_specialities__speciality__slug__in'] = speciality_slugs

    if available_today:
        today_date = datetime.now()
        day_name = today_date.strftime("%A")
        query['doctor_available_days__isnull'] = False
        query['doctor_timeslots__start_time__isnull'] = False
        query['doctor_available_days__day'] = day_name
        query['doctor_timeslots__start_time__gte'] = today_date.time()

    if video_consultaion:
        query['doctor_timeslots__availability_type'] = 'Online'

    if discounts:
        query['doctor_timeslots__discount__gt'] = 0

    if doctor_gender:
        if doctor_gender == 'MALE':
            query['user__gender'] = 'Male'
        elif doctor_gender == 'FEMALE':
            query['user__gender'] = 'Female'

    if most_experienced:
        order_query.append('working_since')

    if lowest_fee:
        annotate_query['fees'] = Min('doctor_timeslots__fee')
        order_query.append('fees')
        reverse = True

    if highest_rating:
        annotate_query['total_rating'] = Sum('doctor_reviews__rating')
        order_query.append('total_rating')

    if highest_rating:
        annotate_query['total_reviews'] = Count('doctor_reviews__rating')
        order_query.append('total_reviews')

    context = {
        'is_search_page' : True,
        'remove_footer' : True
    }
    if searchText.lower().startswith('dr'):
        searchText = searchText.replace('dr ', '')

    doctors = Doctor.objects.prefetch_related(
        'doctor_medias',
        'doctor_reviews',
        'doctor_available_days',
    ).annotate(**annotate_query).filter(
        Q(heading__icontains = searchText) |
        Q(desc__icontains = searchText) |
        Q(name__icontains = searchText),
        is_deleted = False,
        is_blocked = False,
        is_active = True,
        **query
    ).distinct().order_by(*order_query)

    if searchText:
        doctors = doctors.annotate(
                name_h=SearchHeadline("name", searchText, start_sel="<span class='bg-[#fff199] px-2'>", stop_sel="</span>",),
                desc_h=SearchHeadline("desc", searchText, start_sel="<span class='bg-[#fff199] px-2'>", stop_sel="</span>",),
        )
        for d in doctors:
            d.name = d.name_h
            d.desc = d.desc_h

    context['doctors'] = doctors[:: -1 if reverse else 1][:10]
    # hospital_timeslots__isnull=False

    context['DoctorsCount'] = len(doctors)
    context['searchedSpecialities'] = speciality_slugs
    context['searchedDiseases'] = disease_slugs
    context['searchedDiseases'] = disease_slugs
    context['searchedHospitals'] = hospital_slugs
    return render(request, 'Search/Updated_FilterPage.html', context=context)

def emergencyPage(request):
    return render(request, 'Emergency/index.html', {'hide_emergency_icon' : True})
