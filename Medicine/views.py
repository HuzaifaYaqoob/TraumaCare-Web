from django.shortcuts import render

# Create your views here.


def AllMedicinesPage(request):
    return render(request, 'Medicine/AllMedicinePage.html')


def SingleMedicineViewPage(request, id):
    return render(request, 'Medicine/SingleMedicineViewPage.html')