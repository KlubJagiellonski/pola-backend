from django.http import HttpResponse
from django.shortcuts import render

def product(request, barcode):

    return HttpResponse("You're looking at question %s." % barcode)
