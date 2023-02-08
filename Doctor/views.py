from django.shortcuts import render

# Create your views here.


def DoctorSearchPage(request):
    return render(request, 'Doctor/doctor_search_page.html')

def DoctorProfilePage(request):
    return render(request, 'Doctor/doctorprofile.html')