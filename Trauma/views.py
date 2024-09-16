

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings

from Doctor.models import Doctor
from Trauma.models import Speciality, Disease
from django.db.models import Case, When, Min, Sum, Q, Count
from rest_framework.authtoken.models import Token
from Secure.models import ApplicationReview
from Blog.models import BlogPost

from datetime import datetime

def homePage(request):
    context = {}

    doctors = Doctor.objects.all()
    context['doctors'] = doctors
    context['blog_posts'] = BlogPost.objects.annotate(media = Count('blog_post_medias')).filter(media__gt = 0).order_by('-created_at')[:8]
    context['application_reviews'] = ApplicationReview.objects.filter(is_deleted = False, is_blocked=False).order_by('-rating')[0:20]
    return render(request, 'Home/index.html', context)


def onboarding(request):
    onboarding_type = request.GET.get('onboarding_type',  None)
    if onboarding_type == None:
        return redirect('/onboarding/?onboarding_type=doctor')
    
    if onboarding_type == 'doctor':
        return render(request, 'DoctorOnboarding.html')
    elif onboarding_type == 'hospital':
        return render(request, 'HospitalOnboarding.html')

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
    disease_slug = request.GET.get('disease', None)
    speciality_slug = request.GET.get('speciality', None)

    query = {
    }

    annotate_query = {}
    order_query = []
    reverse = False

    if disease_slug:
        query['doctor_disease_specialities__disease__slug__iexact'] = disease_slug.lower()

    if speciality_slug:
        query['doctor_specialities__speciality__slug__iexact'] = speciality_slug.lower()

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

    doctors = Doctor.objects.annotate(**annotate_query).filter(
        Q(email__icontains = searchText) |
        Q(heading__icontains = searchText) |
        Q(slug__icontains = searchText) |
        Q(desc__icontains = searchText) |
        Q(doctor_specialities__speciality__name__icontains = searchText) |
        Q(doctor_specialities__speciality__speciality_type__icontains = searchText) |
        Q(doctor_specialities__speciality__description__icontains = searchText) |
        Q(doctor_specialities__speciality__slug__icontains = searchText) |
        Q(doctor_specialities__speciality__tag_line__icontains = searchText) |
        Q(doctor_disease_specialities__disease__name__icontains = searchText) |
        Q(doctor_disease_specialities__disease__description__icontains = searchText) |
        Q(doctor_disease_specialities__disease__slug__icontains = searchText) |
        Q(doctor_disease_specialities__disease__tag_line__icontains = searchText) |
        Q(doctor_available_days__day__icontains = searchText) |
        Q(doctor_hospital_timeslots__hospital__name__icontains = searchText) |
        Q(doctor_hospital_timeslots__hospital__description__icontains = searchText) |
        Q(doctor_hospital_timeslots__hospital__slug__icontains = searchText) |
        Q(doctor_hospital_timeslots__location__name__icontains = searchText) |
        Q(doctor_hospital_timeslots__location__street_address__icontains = searchText) |
        Q(doctor_hospital_timeslots__location__city__name__icontains = searchText) |
        Q(name__icontains = searchText),
        is_deleted = False,
        is_blocked = False,
        is_active = True,
        **query
    ).distinct().order_by(*order_query)


    context['doctors'] = doctors[:: -1 if reverse else 1]
    context['count'] = len(doctors)
    return render(request, 'Search/Updated_FilterPage.html', context=context)

def emergencyPage(request):
    return render(request, 'Emergency/index.html', {'hide_emergency_icon' : True})
