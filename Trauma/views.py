

from django.shortcuts import render


def homePage(request):
    return render(request, 'Home/index.html')

def email_view(request):
    path = request.GET.get('path')
    return render(request, path)


def FeedPage(request):
    return render(request, 'Feed/feedPage.html')

def SpecialitiesPage(request):
    return render(request, 'Speciality/specialities.html')

def SingleSpecialityPage(request):
    return render(request, 'Speciality/speciality.html')

def test(request):
    return render(request, 'prescription.html')

def CartPage(request):
    return render(request, 'User/cart.html')

def searchFilterPage(request):
    # return render(request, 'Search/booklabtest.html')
    context = {
        'is_search_page' : True,
        'remove_footer' : True
    }
    return render(request, 'Search/Updated_FilterPage.html', context=context)

