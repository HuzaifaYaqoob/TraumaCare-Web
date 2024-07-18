from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required(login_url='/auth/login/')
def AskDoctorMainPage(request):
    return render(request, 'qa/AskDoctorMainPage.html')