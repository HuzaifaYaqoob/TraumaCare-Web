

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.conf import settings

from Doctor.models import Doctor, DoctorMedia
from Trauma.models import Speciality, Disease, State, Country, City
from django.db.models import Case, When, Min, Sum, Q, Count
from rest_framework.authtoken.models import Token
from Secure.models import ApplicationReview
from Blog.models import BlogPost

from Hospital.models import Hospital, HospitalLocation, LocationContact, HospitalMedia

from Profile.models import Profile

from datetime import datetime
from Product.models import Product

def homePage(request):
    context = {}

    doctors = Doctor.objects.filter(
        is_active = True,
        is_deleted = False,
        is_blocked = False,
    )
    print(doctors)
    context['doctors'] = doctors[:8]
    context['blog_posts'] = BlogPost.objects.annotate(media = Count('blog_post_medias')).filter(media__gt = 0).order_by('-created_at')[:4]
    # .annotate(media = Count('blog_post_medias')).filter(media__gt = 0)
    context['application_reviews'] = ApplicationReview.objects.filter(is_deleted = False, is_blocked=False).order_by('-rating')[0:20]
    context['medicines'] = Product.objects.filter(
        is_active = True,
        is_deleted = False,
        is_blocked = False
    ).order_by('?')[:10]
    return render(request, 'Home/index.html', context)


# https://www.facebook.com/sharer.php?u=https://ailaaj.pk/products/medeco-insulin-syringe-1cc-31g-x-8mm-10s

def onboarding(request):
    onboarding_type = request.GET.get('onboarding_type',  None)
    if onboarding_type == None:
        return redirect('/onboarding/?onboarding_type=doctor')
    
    if request.method == 'POST':
        if onboarding_type == 'doctor':
            full_name = request.POST.get('full_name', None)
            gender = request.POST.get('gender', None)
            speciality = request.POST.get('speciality', None)
            about = request.POST.get('about', None)
            working_since = request.POST.get('working_since', None)
            profile_image = request.FILES.get('profile_image', None)
            pmc_document = request.FILES.get('pmc_document', None)

            f_name, *l_name = f'{full_name} '.split(' ')
            l_name = ' '.join(l_name)
            d_p = Profile.objects.create(user = request.user, first_name = f_name, last_name = l_name, full_name = full_name, profile_type = 'Doctor', profile_image = profile_image,)
            doctor = Doctor.objects.create(
                user = request.user,
                profile = d_p,
                name = full_name,
                heading = speciality,
                # dial_code
                mobile_number = request.user.mobile_number,
                working_since = datetime.strptime(working_since, '%m/%d/%Y').date(),
                desc = about,
            )
            DoctorMedia.objects.create(
                doctor = doctor,
                file_type = 'Profile Image',
                file = profile_image
            )
            if pmc_document:
                DoctorMedia.objects.create(
                    doctor = doctor,
                    file_type = 'License',
                    file = pmc_document
                )
            
            request.user.gender = gender
            request.user.save()
            messages.success(request, 'Onboarding Successful!')
            return redirect('/')
            
        else:
            hospital_name = request.POST.get('hospital_name', None)
            hospital_email = request.POST.get('hospital_email', None)
            address_title = request.POST.get('address_title', None)
            address_state = request.POST.get('address_state', None)
            address_city = request.POST.get('address_city', None)
            address = request.POST.get('address', None)
            hospital_image = request.FILES.get('hospital_image', None)

            f_name, *l_name = f'{hospital_name} '.split(' ')
            l_name = ' '.join(l_name)

            h_p = Profile.objects.create(user = request.user, first_name = f_name, last_name = l_name, full_name = hospital_name, email = hospital_email, profile_type = 'Hospital', profile_image = hospital_image,)
            hospital = Hospital.objects.create(user = request.user, profile = h_p, facility_type = Hospital, name = hospital_name,)
            hops_l = HospitalLocation.objects.create(hospital = hospital, name = address_title,street_address = address, country = Country.objects.get(name__iexact = 'pakistan',), state = State.objects.get(id = address_state), city = City.objects.get(id = address_city),)
            LocationContact.objects.create(hospital = hospital, location = hops_l, contact_type = "EMAIL", contact_title = 'Contact Email', email = hospital_email,)
            HospitalMedia.objects.create(hospital = hospital, file_type = 'Profile Image', file = hospital_image)

            messages.success(request, 'Onboarding Successful!')
            return redirect('/')
    
    context = {}
    if onboarding_type == 'doctor':
        if request.user.has_doctor_profile:
            messages.info(request, 'Doctor Profile Already Exists!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        return render(request, 'DoctorOnboarding.html', context)
    elif onboarding_type == 'hospital':
        if request.user.has_hospital_profile:
            messages.info(request, 'Hospital Profile Already Exists!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
        context['states'] = State.objects.filter(is_deleted = False, is_active = True, country__name__icontains = 'pakistan').order_by('name')
        context['cities'] = City.objects.filter(is_deleted = False, is_active = True, country__name__icontains = 'pakistan').order_by('name')
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
