from django.shortcuts import render, redirect

# Create your views here.


def AllMedicinesPage(request):
    return redirect('PharmacyLandingPage')


def SingleMedicineViewPage(request, id):
    return render(request, 'Medicine/SingleMedicineViewPage.html')